from typing import Optional

from .types import Quality, CriteriaTreeElement, Criterion, TaskGroup, Task, CriteriaTree


def to_color_hex_string(color):
    """
    Convert a color object to a hex string
    """
    if isinstance(color, str):
        return color
    return f"#{color.red:02x}{color.green:02x}{color.blue:02x}"


def should_hide_code(element: CriteriaTreeElement | str | dict) -> bool:
    """
    Check if a tree element should be hidden in the output
    """
    if isinstance(element, str):
        return element.startswith('_')
    if isinstance(element, dict):
        code: Optional[str] = element.get('code', None)
        if code is None:
            raise ValueError("Element must have a 'code' key")
        return code.startswith('_')
    return element.code.startswith('_')


def get_qualified_name(element: Quality | Criterion | TaskGroup | Task | dict) -> str:
    """
    Get the qualified name of a tree element, which is the title with the code prepended if it is different
    """
    if isinstance(element, dict):
        title, code = (element.get('title', None), element.get('code', None))
        if title is None or code is None:
            raise ValueError("Element must have 'title' and 'code' keys")
    else:
        title, code = element.title, element.code
    if code.startswith('_'):
        code = code[1:]
    if element.title == code:
        return element.title
    return f"{code} {element.title}"


def resolve_code(element: CriteriaTreeElement | str | dict) -> str:
    """
    Get the code for a tree element, stripping away unnecessary characters
    """
    if isinstance(element, str):
        resolved_code = element
    elif isinstance(element, dict):
        resolved_code = element.get('code', None)
        if resolved_code is None:
            raise ValueError("Element must have a 'code' key")
    else:
        resolved_code = element.code
    return resolved_code[1:] if resolved_code.startswith('_') else resolved_code


def find_in_tree(tree: CriteriaTree, code: str) -> Optional[CriteriaTreeElement]:
    """
    Find an element in the criteria tree by its code
    """
    for quality in tree.qualities:
        if quality.code == code:
            return quality
        for criteria in quality.items:
            if criteria.code == code:
                return criteria
            for task_group in criteria.items:
                if task_group.code == code:
                    return task_group
                for task in task_group.items:
                    if task.code == code:
                        return task
                    for task_item in task.items:
                        if task_item.code == code:
                            return task_item
    return None
