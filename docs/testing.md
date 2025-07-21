# Test setup

This repository uses:

- uv to control the environments (so that test dependencies don't leak into
  prod)
- pytest as the test runner
- coverage as the package for ensuring appropriate coverage

The important files controlling the test process are:

- pyproject.toml - stores the environments, script commands
- src/**/*.py contains the files to test
- tests/test_*.py contains normal unit tests
- tests/integration/test_*.py contains end-to-end integration tests (marked with
  @pytest.mark.integration)
- tests/conftest.py stores the pytest global fixtures

Where possible, configuration is stored directly in the pyproject.toml file. If
the tool doesn't support it, then additional information may be stored elsewhere
(e.g. a .coveragerc location)

# Testing philosophy

Unit testing should strive to primarily serve the developer for understanding
how the code works. A primary motivation should serve as documentation for a
particular function or API call. How is the class intended to be used? What are
the data types expected? All major parts of the code should have at least one
test which ensures the golden path is covered.

Besides the golden path, there may be various permutations of inputs, or
side-effects which affect the behavior of the function. Since checking for error
conditions can be tedious, unit tests should also verify that every single error
path is handled correctly.

Lastly, unit tests should describe a specification for the desired behavior of
the function. These should describe the scenario, and the behavior that is
expected to happen. These specification tests should allow a developer to
re-create the production behavior just by reading and understanding these unit
tests. They're not intended to directly capture a particular implementation
algorithm, or edge case that might not apply in a different scenario.

Code coverage is an important metric to strive for, but it is not the be-all
measure of success for a test library. Code coverage should always be looked at,
to understand which gaps are missing. If the gap is due to an untested error
condition, then that is a good candidate for either writing a new test, and/or
restructuring the production code to consolidate code flows or make an error
case easier to test. Otherwise, consider if the missing coverage is due to a gap
in description about the function behavior, or is it rather an implementation
detail? If it's the latter, consider moving complicated logic into an
implementation-specific helper function to fully validate it, or ignore testing
it.

# Best practices

- Have small unit tests, rather than one large test that does multiple things
- Use fixtures to describe what valid data looks like
- Create bad data by modifying the good data (so you know it's valid except this
  one thing)
- Use data-driven tests to help keep the code DRY
- Focus on usability of the tests - are they clear in what's being tested?
- Avoid over-mocking as it's a sign of production code that needs to be
  refactored
- See https://github.com/astral-sh/uv/issues/7260 for how to setup uv to work
  with `uv run pytest`

# Example

This section describes a HTTP endpoint that we'd like to add tests for, and what
a good test suite would look like. Suppose we had an endpoint to add a new book
to a library:

```python
@app.post("/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Add a new book to the library.
    
    Args:
        book: Book data to create
        db: Database session
        
    Returns:
        Created book with ID and timestamps
        
    Raises:
        HTTPException: If ISBN already exists or validation fails
    """
    db_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        publication_year=book.publication_year
    )
    
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e) and "isbn" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail=f"Book with ISBN {book.isbn} already exists"
            )
        raise HTTPException(
            status_code=500,
            detail="Database constraint violation"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create book in database"
        )
```

A good test suite for this function might look like this:

```python
@pytest.fixture
def good_book():
  # An example book that has valid fields
  # If the API is ever updated to have more fields,
  # we'll only need to change this reference, and not the rest of the tests
  return Book(...)

def test_create_book(good_book):
  # Golden path test
  # posts the book, ensures the status code is 200
  # calls GET /books/:id and makes sure the data is available

@pytest.mark.parameterize("name,changes", [
  ("missing_isbn", {"isbn": None}),
  ("invalid_format"{"isbn": "wrong_format"}),
  ...
])
def test_invalid_books(good_book, name, changes):
  # Validating all of the relevant error conditions 
  # Ensures sanitization is correct, now and in the future
  book = good_book.dict()
  new_book = good book / changes
  response = client.post("/books", json=book_data)
  assert(response.status_code == 400)

def test_duplicate_isbn(good_book):
  response = client.post("/books", json=good_book)
  assert(response.ok)
  other_book = good_book / {"name": "other_name"}
  response = client.post("/books", json=other_book)
  assert(response.status_code == 400)
  # Ensure the original book isn't changed
  ...
```
