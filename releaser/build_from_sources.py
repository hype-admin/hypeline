import os
import re
import json
import zipfile


projectPath = os.getcwd()

def get_version_from_name(name: str) -> str:
    search: re.Match | None = re.search(r"_v(\d{1,}(\.\d{1,}){0,})", name, re.IGNORECASE)

    if search == None:
        return ''
    else:
        return search.group(1)



def get_wip_version_from_name(name: str) -> str:
    search: re.Match | None = re.search(r"_wip(\d{1,})", name, re.IGNORECASE)

    if search == None:
        return ''
    else:
        return search.group(1)


def get_all_versions(baseLink: str):

    if r"{all}" in baseLink:
        marker = r"{all}"
    else:
        marker = '*'

    baseName = baseLink.replace(marker, '')

    if os.path.isdir(baseName):
        files = [os.path.join(baseName, x) for x in os.listdir(baseName)]

    else:
        relativeFolder = os.path.dirname(baseName)
        fileBaseNameContent = [x for x in baseLink.split(marker) if x != '']

        if len(fileBaseNameContent) == 1:
            baseFileName = fileBaseNameContent[0]
            files = [os.path.join(baseName, x) for x in os.listdir(relativeFolder) if baseFileName in x]

        elif len(fileBaseNameContent) == 2:
            suffixName = fileBaseNameContent[0]
            prefixName = fileBaseNameContent[1]
            files = [os.path.join(baseName, x) for x in os.listdir(relativeFolder) if suffixName in x and prefixName in x]

        else:
            print(f"ERRO: o padrão {baseLink} possui mais de uma palavra chave {{all}} ou *")
            return

    if len(files) == 0:
        print(f"ERRO: nenhum arquivo encontrado no padrão {baseLink}")
        return

    return files



def get_latest_file_version(file: str):
    splitedName = [part for part in file.split(r"{latest}") if part != '']
    fileBaseFolder, fileBaseName = os.path.split( splitedName[0] )
    fileBaseFolder = os.path.abspath(fileBaseFolder)

    if len(splitedName) == 1:
        filesList = [x for x in os.listdir(fileBaseFolder) if x.startswith(fileBaseName)]
    elif len(splitedName) == 2:
        filesList = [x for x in os.listdir(fileBaseFolder) if x.startswith(fileBaseName) and x.endswith(splitedName[-1])]
    else:
        print(f"""ERRO: não foi achado nenhum arquivo no padrão "{fileBaseName}" na pasta "{fileBaseFolder}". """)
        return

    filesList.sort()
    latestFile = filesList[-1]

    return os.path.join('.', latestFile)




def build_from_json_file(jsonfile: str):

    if not jsonfile.endswith('.json'):
        jsonPath = os.path.join(projectPath, jsonfile + '.json')
    else:
        jsonPath = os.path.join(projectPath, jsonfile)

    if not os.path.exists(jsonPath):
        print(f"""ERRO: não foi encontrado um arquivo chamado "{jsonfile}.json" na pasta {projectPath}""")
        return

    _build(jsonPath)



def build_from_current_path():
    print(f"building from current path: {projectPath}")

    if os.path.exists('./releases.json'):
        jsonPath = os.path.join(projectPath, 'releases.json')
        jsonPath = os.path.abspath(jsonPath)

    elif os.path.exists('./release.json'):
        jsonPath = os.path.join(projectPath, 'release.json')
        jsonPath = os.path.abspath(jsonPath)

    else:
        print(f"""ERRO: não foi encontrado um arquivo chamado "releases.json" na pasta {projectPath}""")
        return

    _build(jsonPath)



def resolve_archive_base_name(name: str):
    filename = name

    if r"{latest}" in name:
        filename = get_latest_file_version(filename)

        if filename == None:
            print(f"ERRO: arquivo {name} não encontrado.")
            return

    versionNumber = get_version_from_name(filename)
    wipNumber = get_wip_version_from_name(filename)

    fileBaseName = os.path.basename(filename)
    fileBaseName = os.path.splitext(fileBaseName)[0]
    fileBaseName = fileBaseName.split('_v')[0]

    if wipNumber and versionNumber:
        filename = f"{fileBaseName}_v{versionNumber}_wip{wipNumber}"

    elif wipNumber and not versionNumber:
        filename = f"{fileBaseName}_wip{wipNumber}"

    elif not wipNumber and versionNumber:
        filename = f"{fileBaseName}_v{versionNumber}"

    else:
        filename = fileBaseName

    return filename




def _build(jsonPath):
    with open(jsonPath, 'r') as file:
        buildsDict: dict = json.load(file)

    filesDict = buildsDict['files']

    archiveBaseName = resolve_archive_base_name(buildsDict['archive.basename'])

    for buildName in filesDict:

        archiveName = f"{archiveBaseName}_{buildName}"

        print("Gerando a release:", buildName)
        for link in filesDict[buildName]:

            if r"{latest}" in link:
                link = get_latest_file_version(link)
                if link == None:
                    continue

            if r"{all}" in link or '*' in link:
                files = get_all_versions(link)

                for file in files:
                    link = file.replace('\\', '/')
                    print("\t", "Adicionando:", link)
                    add_file_to_archive(link, archiveName)

            else:
                link = link.replace('\\', '/')
                print("\t", "Adicionando:", link)
                add_file_to_archive(link, archiveName)



def add_file_to_archive(file, archiveName):
    if not os.path.exists('./releases'):
        os.mkdir('./releases/')

    with zipfile.ZipFile(f"./releases/{archiveName}.zip", "a") as zip_file:
        zip_file.write(file)

