import xml.etree.ElementTree as ET
tree = ET.parse('input.pom')
root = tree.getroot()
ns = root.tag.split('}')[0].strip('{')

for dep in root.findall("./{" +ns+ "}dependencyManagement/{" + ns + "}dependencies/{"+ns+ "}dependency"):
  groupId = dep.find("./{"+ns+ "}groupId").text
  artifactId = dep.find("./{"+ns+ "}artifactId").text
  version = dep.find("./{"+ns+ "}version").text
  classifierElem = dep.find("./{"+ns+ "}classifier")
  if classifierElem is not None:
    classifier = classifierElem.text
  else:
    classifier = None

  exclusions = []
  for exclusionElem in dep.findall("./{"+ns+ "}exclusions/{"+ns+ "}exclusion"):
    exclGroupId = exclusionElem.find("./{"+ns+ "}groupId").text
    exclArtifactId = exclusionElem.find("./{"+ns+ "}artifactId").text

  if len(exclusions) == 0 and classifier is None:
    print("\"" + groupId + ":" + artifactId + ":" + version + "\",")
  else:
    print("maven.artifact(group=\"" + groupId + "\",")
    print("  artifact = \"" + artifactId + "\"," )
    print("  version = \"" + version + "\",")
    if classifier is not None:
      print("  classifier = \"" + classifier + "\",")
    if len(exclusions) > 0:
      print("  exclusions = [")
      for x in exclusions:
        print("    \"" + x + "\",")
      print("  ],")
    print("),")




