class ParseError(SyntaxError):
    def __init__(self, message: str, position: int) -> None:
        self.message = message
        self.position = position
        super().__init__(f"{message} at {position}")


class ParseEOFError(ParseError):
    def __init__(self, position: int) -> None:
        super().__init__("Unexpected end of file", position)


class Reader:
    def __init__(self, data) -> None:
        self.offset = 0
        self.data = data

    # Skip some characters
    def forward(self, offset: int = 1):
        self.offset += offset
        if self.offset > len(self.data):
            self.offset = len(self.data)
            raise self.eof_error()

    # Go back for some characters
    def back(self, offset: int = 1):
        self.forward(-offset)

    # Check if it's an end of file
    def is_eof(self) -> bool:
        if self.offset >= len(self.data):
            self.offset = len(self.data)
            return True

        return False

    # Read one character ( doesn't go forward )
    def read(self) -> str:
        if self.is_eof():
            raise self.eof_error()
        return self.data[self.offset]

    def eof_error(self) -> ParseEOFError:
        return ParseEOFError(self.offset)

    def syntax_error(self, message: str) -> ParseError:
        return ParseError(message, self.offset + 1)
