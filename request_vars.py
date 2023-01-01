

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
            'name': 'Сортировка',
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
        'project': {
            'name': 'Проект',
            'type': 'select',
            'field_name': 'project',
            'list': [],
            'value': '',
            'sel_value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сортировка',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
    }

    dTaskFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'group': {
            'name': 'Проект',
            'type': 'select',
            'field_name': 'group',
            'list': [],
            'value': '',
            'sel_value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сортировка',
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
        {"name":"create-project", "cls":"bi-file-plus", "btn_cls": "btn-success"},
        {"name":"edit-project", "cls":"bi-pencil", "btn_cls": "btn-secondary"},
        {"name":"remove-project", "cls":"bi-trash", "btn_cls": "btn-danger"},
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

    dProjectFieldsV={}
    dGroupFieldsV={}
    dTaskFieldsV={}

    sBaseURL = ""

    sSearchProject = ""

    sSelectProject = ""
    sSelectGroup = ""
    sSelectTask = ""
    sSelectFile = ""

    sEditGroup = ""
    sEditTask = ""
    sEditProject = ""

    sCreateGroup = ""
    sCreateTask = ""
    sCreateProject = ""

    oTaskComments = []
    oTaskFiles = []

    lAllTasks = []

    sToggleFilesListType = ""
    sToggleTaskTab = ""
    
    sSelectProjectMode = ""

class SessionVars:
    sSelectProject = ""
    sSelectGroup = ""
    sSelectTask = ""
    sSelectFile = ""