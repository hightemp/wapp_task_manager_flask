

class RequestVars:
    dProjectFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сорт',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
    }

    dGroupFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сорт',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
        'project': {
            'name': 'Проект',
            'type': 'select',
            'field_name': 'project',
            'list': [],
            'value': '',
        },
    }

    dTaskFields = {
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сорт',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
        'a_html': {
            'name': 'Описание HTML',
            'type': 'textarea',
            'field_name': 'a_html',
            'value': '',
        },
        'a_markdown': {
            'name': 'Описание Markdown',
            'type': 'textarea',
            'field_name': 'a_markdown',
            'value': '',
        },
    }

    dClasses = {
        'group': 'Group',
        'category': 'Category',
        'account': 'Account',
    }

    aProjectsButtons = [
        {"name":"reload", "cls":"bi-arrow-repeat", "btn_cls": "btn-primary"},
        {"name":"create_project", "cls":"bi-file-plus", "btn_cls": "btn-success"},
        {"name":"edit_project", "cls":"bi-pencil", "btn_cls": "btn-secondary"},
        {"name":"remove_project", "cls":"bi-trash", "btn_cls": "btn-danger"},
    ]

    sGroupFilter = ''
    sCategoryFilter = ''
    sAccountFilter = ''

    oProjects={}
    oGroups={}
    lTasks = []

    oProject={}
    oGroup={}
    oTask={}

    sBaseURL = ""

    sSelectProject = ""
    sSelectGroup = ""
    sSelectTask = ""
    sSelectFile = ""

    sEditGroup = ""
    sEditTask = ""
    sEditProject = ""