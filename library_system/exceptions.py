class LibraryError(Exception):
    """Base exception for all library errors"""
    pass

# 1. For missing things
class NotFoundError(LibraryError):
    """Raised when a book or resource isn't found"""
    pass

# 2. For state issues (borrowed/available)
class StateError(LibraryError):
    """Raised when operation can't be done due to current state"""
    pass

# 3. For empty lists/collections (optional - could use StateError)
class EmptyError(LibraryError):
    """Raised when a collection is empty"""
    pass
