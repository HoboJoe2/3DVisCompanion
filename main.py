import dearpygui.dearpygui as dpg
import subprocess

def convert_file(file_path):
    batch_file = ["convert.bat", file_path]

    # Run the batch file (copied from chatgpt, not sure what some of this means)
    try:
        result = subprocess.run(batch_file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Output:\n", result.stdout)
        print("Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def runGUI():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=300)

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")
        dpg.add_button(label="Save")
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

runGUI()