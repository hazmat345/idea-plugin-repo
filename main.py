import xml.etree.ElementTree as ET
import aiofiles
from fastapi import FastAPI, Form, UploadFile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def create_upload_file(
        file: UploadFile, id: str = Form(), url: str = Form(), version: str = Form()
):
    # Save off the file
    async with aiofiles.open(f"files/{file.filename}", 'wb') as f:
        content = await file.read()
        await f.write(content)

    # Deal with the xml stuff
    tree = ET.parse('updatePlugins.xml')
    plugins = tree.getroot()

    plugin = ET.SubElement(plugins, 'plugin')
    plugin.set('id', id)
    plugin.set('url', url)
    plugin.set('version', version)

    name = ET.SubElement(plugin, "name")
    name.text = file.filename

    idea_version = ET.SubElement(plugin, "idea_version")
    idea_version.set("since-build", "222.0")
    # idea_version.set("until-build", "")

    # Indent and write out the updated xml file
    ET.indent(tree)
    async with aiofiles.open("updatePlugins.xml", "wb") as f:
        await f.write(ET.tostring(plugins))

    return
