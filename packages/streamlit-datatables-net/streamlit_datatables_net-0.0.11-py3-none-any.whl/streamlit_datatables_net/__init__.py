import os
import streamlit.components.v1 as components
import streamlit as st
import json
from typing import List, Dict

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if _RELEASE:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "streamlit_datatables_net", path=build_dir)

else:
    _component_func = components.declare_component(
        "streamlit_datatables_net",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.


def st_datatable(props: Dict, table_id: str = None, class_name: str = None, js_scripts: List[str] = None, stylesheets: List[str] = None, key=None):
    """Create a new instance of "st_datatable".

    Parameters
    ----------
    props: dict
        The props to set the data attributes and configuration options for the datatable.
    class_name: str or None
        An optional str of class names to apply to the datatable (e.g., 'compact hover').
    js_scripts: list or None
        An optional list of urls for javascripts to apply to the datatable.
    stylesheets: list or None
        An optional list of urls for stylesheets to apply to the datatable.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict
        The API response from the datatable.

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(
        props=props, table_id=table_id, class_name=class_name, js_scripts=js_scripts, stylesheets=stylesheets, key=key, default={})

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


if not _RELEASE:
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    data = [
        {
            "id": "1",
            "name": "Tiger Nixon",
            "position": "System Architect",
            "salary": 320800,
            "start_date": "2011/04/25",
            "office": "Edinburgh",
            "extn": "5421",
        },
        {
            "id": "2",
            "name": "Garrett Summers",
            "position": "Accountant",
            "salary": 170750,
            "start_date": "2011/07/25",
            "office": "Tokyo",
            "extn": "8422",
        },
    ]

    columns = [
        {"data": "name", "title": "Name"},
        {"data": "position", "title": "Position"},
        {"data": "office", "title": "Office"},
        {"data": "salary", "title": "Salary",
            "render": ['number', ',', '.', 0, '$']},
        {"data": "", "title": "Actions",
            "column_type": "actions", "actions": ["view", "edit", "delete", "pdf"]},
        {"data": "", "title": "Open", "column_type": "url",
            "url": "https://google.com", "display_text": "Google"},
        {"data": "edit_link", "title": "Edit Link"},
        {"data": "extn", "title": "extn", "column_type": "render",
            "javascript": "function(data, type, row, meta) { return '<a href=\"' + data + '\">Download</a>'; }"},
    ]

    props = {}
    for item in data:
        item["edit_link"] = "https://google.com"
    props["data"] = data
    props["columns"] = columns

    stylesheets = [
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://cdn.datatables.net/v/dt/jq-3.7.0/jszip-3.10.1/dt-1.13.6/b-2.4.1/b-html5-2.4.1/b-print-2.4.1/r-2.5.0/datatables.min.css"]

    js_scripts = [
        "https://cdn.datatables.net/v/dt/jq-3.7.0/jszip-3.10.1/dt-1.13.6/b-2.4.1/b-html5-2.4.1/b-print-2.4.1/r-2.5.0/datatables.min.js"]

    class_name = "compact row-border hover"

    col_l, col_m, col_r = st.columns([1, 10, 1])
    with col_m:
        dt_response = st_datatable(
            props, table_id="my_datatable", class_name=class_name, js_scripts=js_scripts, stylesheets=stylesheets, key="bar")
        st.write(dt_response)
