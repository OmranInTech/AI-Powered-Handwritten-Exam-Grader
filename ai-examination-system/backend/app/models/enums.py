from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class ExamMode(str, Enum):
    DIGITAL = "DIGITAL"
    HANDWRITTEN = "HANDWRITTEN"


class QuestionType(str, Enum):
    MCQ = "MCQ"
    TRUE_FALSE = "TRUE_FALSE"
    SHORT_ANSWER = "SHORT_ANSWER"
    ESSAY = "ESSAY"
    FILL_BLANK = "FILL_BLANK"


class GradingPolicy(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    TEACHER_APPROVAL = "TEACHER_APPROVAL"


class ExamStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    COMPLETED = "COMPLETED"


class SubmissionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    EVALUATED = "EVALUATED"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"

