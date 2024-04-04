laraImport("weaver.Query");
laraImport("lara.Io");

const path = "C:/Users/JBispo/Work/Repos/Lab/llm-code-patcher/cmake_example/";

for (const func of Query.search("function")) {
  const file = func.ancestor("file");

  const filename = file.name + "_" + func.name + ".c";
  Io.writeFile(Io.getPath(path, filename), func.code);
}
