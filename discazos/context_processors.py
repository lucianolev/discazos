from discazos import __last_update__

def VersionContextProcessor(request):
    return { "PROJECT_LAST_UPDATE": __last_update__ }