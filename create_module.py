import os


def create_module_files(module_name: str):
    module_name_titlecase = module_name.title()
    folder_path = os.path.join("apps", module_name)
    os.makedirs(folder_path)

    files = ["Model", "Repository", "Routes", "Schema", "Service"]
    for file_name in files:
        file_path = os.path.join(folder_path, f"{module_name_titlecase}{file_name}.py")
        with open(file_path, "w") as file:
            file.write(f"# {module_name_titlecase}{file_name}.py\n")
            file.write(f"class {module_name_titlecase}{file_name}:\n")
            file.write(f"    pass\n")


if __name__ == "__main__":
    module_name = input("Enter the module name: ")
    create_module_files(module_name)
