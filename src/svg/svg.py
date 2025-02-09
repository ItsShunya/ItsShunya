from lxml import etree

def svg_overwrite(filename, age_data, commit_data, star_data, repo_data, contrib_data, follower_data, loc_data):
    """
    Parse SVG files and update elements with my age, commits, stars, repositories, and lines written
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
    Updates and formats the text of the element, and modifes the amount of dots in the previous element to justify the new text on the svg
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
    Finds the element in the SVG file and replaces its text with a new value
    """
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text
