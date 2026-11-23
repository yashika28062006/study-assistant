
"""Custom tools for the Study Planner Assistant."""

import ast
import operator
from datetime import date, datetime

from langchain_core.tools import tool


# -------------------------------
# Starter calculator functionality
# -------------------------------

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left = _eval(node.left)
        right = _eval(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("That power is too large.")

        return _OPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))

    raise ValueError("Only numbers and + - * / ** % are allowed.")


@tool
def calculator(expression: str) -> str:
    """Calculate a maths expression such as '12 * (3 + 4)'."""

    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Could not calculate: {e}"


@tool
def today() -> str:
    """Return today's date."""

    return date.today().isoformat()


# -------------------------------
# CUSTOM TOOL 1: Exam Countdown
# -------------------------------

@tool
def days_until_exam(exam_date: str) -> str:
    """
    Calculate the number of days remaining until an exam.
    Use a date in YYYY-MM-DD format.
    """

    try:
        exam = datetime.strptime(exam_date, "%Y-%m-%d").date()
        remaining = (exam - date.today()).days

        if remaining < 0:
            return f"The exam date has already passed by {abs(remaining)} days."

        if remaining == 0:
            return "Your exam is today! All the best!"

        return f"You have {remaining} days remaining until your exam."

    except ValueError:
        return "Invalid date. Please use YYYY-MM-DD format."


# -------------------------------
# CUSTOM TOOL 2: Study Hour Splitter
# -------------------------------

@tool
def split_study_hours(total_hours: float, subjects: str) -> str:
    """
    Divide available study hours equally among a list of subjects.
    Provide total hours as a number and subjects separated by commas.
    """

    try:
        if total_hours <= 0:
            return "Please enter study hours greater than zero."

        subject_list = [
            subject.strip()
            for subject in subjects.split(",")
            if subject.strip()
        ]

        if not subject_list:
            return "Please provide at least one subject."

        hours_per_subject = total_hours / len(subject_list)

        result = [
            f"Total study hours: {total_hours}",
            f"Number of subjects: {len(subject_list)}",
            f"Hours per subject: {hours_per_subject:.2f}",
            "",
            "Your study plan:"
        ]

        for subject in subject_list:
            result.append(f"- {subject}: {hours_per_subject:.2f} hours")

        return "\n".join(result)

    except (ValueError, AttributeError):
        return "Invalid input. Please provide valid study hours and subjects."


# -------------------------------
# Register all available tools
# -------------------------------

TOOLS = [
    calculator,
    today,
    days_until_exam,
    split_study_hours
]
