# The Python Standard Library.
from lxml import etree

def svg_overwrite(filename, age_data, commit_data, star_data, repo_data, contrib_data, follower_data, loc_data):
    """
    Parse SVG files and update elements with specified data.

    This function reads an SVG file, updates various elements with provided data,
    and writes the modified content back to the file.

    Parameters
    ----------
    filename : str
        Path to the SVG file to be modified.
    age_data : int
        Age data to be displayed.
    commit_data : int
        Commit data to be displayed.
    star_data : int
        Star data to be displayed.
    repo_data : int
        Repository data to be displayed.
    contrib_data : int
        Contribution data to be displayed.
    follower_data : int
        Follower data to be displayed.
    loc_data : list of int
        List containing lines of code data.

    Returns
    -------
    None

    Raises
    ------
    etree.XMLSyntaxError
        If the SVG file cannot be parsed.
    IOError
        If there is an error writing to the file.
    """
    tree = etree.parse(filename)
    print(tree)
    root = tree.getroot()

    justify_format(root, 'commit_data',     commit_data, 22)
    justify_format(root, 'age_data',        age_data, 48)
    justify_format(root, 'star_data',       star_data, 14)
    justify_format(root, 'repo_data',       repo_data, 7)
    justify_format(root, 'contrib_data',    contrib_data)
    justify_format(root, 'follower_data',   follower_data, 10)
    justify_format(root, 'loc_data',        loc_data[2], 9)
    justify_format(root, 'loc_add',         loc_data[0])
    justify_format(root, 'loc_del',         loc_data[1], 6)

    tree.write(filename, encoding='utf-8', xml_declaration=True)

def justify_format(root, element_id, new_text, length=0):
    """
    Update and format the text of an SVG element, adjusting dot justification.

    This function updates the text of the specified SVG element and modifies
    the number of dots in a related element to ensure text justification.

    Parameters
    ----------
    root : etree.Element
        The root element of the SVG document.
    element_id : str
        The ID of the element to be updated.
    new_text : int or str
        The new text to be set. If an integer, it will be formatted with commas.
    length : int, optional
        The target length for justification. If the new text is shorter, dots
        will be added to fill the space (default is 0).

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the element with the specified ID is not found.
    """
    if isinstance(new_text, int):
        new_text = f"{'{:,}'.format(new_text)}"
    new_text = str(new_text)
    find_and_replace(root, element_id, new_text)
    just_len = max(0, length - len(new_text))
    if just_len <= 2:
        dot_map = {0: '', 1: ' ', 2: '. '}
        dot_string = dot_map[just_len]
    else:
        dot_string = ' ' + ('.' * just_len) + ' '
    find_and_replace(root, f"{element_id}_dots", dot_string)

def find_and_replace(root, element_id, new_text):
    """
    Find an SVG element by ID and replace its text content.

    Parameters
    ----------
    root : etree.Element
        The root element of the SVG document.
    element_id : str
        The ID of the element to be found and updated.
    new_text : str
        The new text content to set.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the element with the specified ID is not found.
    """
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text
    else:
        raise ValueError(f"Element with ID '{element_id}' not found.")
