try:
    import struct
    import shutil
    import zipfile
    import py7zr
    import rarfile
    import time
    import os
    import sys
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, PageBreak, Image, Spacer, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from datetime import datetime
except ImportError:
    print("\n...REQUIRED PYTHON MODULES MISSING. Please install dependencies with `pip install -r requirements.txt`\n")
    sys.exit(0)

LUMP_ENTITIES = 0
LUMP_MODELS = 14
HEADER_LUMPS = 17
LUMP_SIZE = 8
HEADER_SIZE = 4 + HEADER_LUMPS * LUMP_SIZE

time_short = datetime.now().strftime("%b_%d-%H_%M_%S")
time_full = datetime.now().strftime(("%A %d %B %Y - %H:%M:%S"))
map_count = 0
spawn_points = []

def iterate(bdel: int, tdel: float, *str: any):
    time.sleep(bdel)
    for char in str:
        print(char, end='', flush=True)
        time.sleep(tdel)
    print()

def generate_3d_plot(spawn_points, minmax_x, minmax_y, minmax_z, output_filename, map_id):
    fig = plt.figure(figsize=(9, 7), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=25, azim=45)

    x_range = minmax_x[1] - minmax_x[0]
    y_range = minmax_y[1] - minmax_y[0]
    z_range = minmax_z[1] - minmax_z[0]
   
    x_offset_percent = 0.1
    y_offset_percent = 0.15
    z_offset_percent = 0.03

    x_offset_percent_medium = 0.1
    y_offset_percent_medium = 0.10
    z_offset_percent_medium = 0.02

    x_offset_percent_small = 0.1
    y_offset_percent_small = 0.05
    z_offset_percent_small = 0.01
   
    if len(spawn_points) < 15:
        for i, (x, y, z) in enumerate(spawn_points, start=1):
            x_adjusted = x + x_range * x_offset_percent
            y_adjusted = y + y_range * y_offset_percent
            z_adjusted = z + z_range * z_offset_percent
            ax.scatter(x, y, z, color='black', s=125, edgecolors='white', linewidth=0.5)  
            ax.text(x_adjusted, y_adjusted, z_adjusted, f"{i}", color='red', fontsize=12,
                ha='center', va='center')
    elif len(spawn_points) >= 15 and len(spawn_points) < 20:
        for i, (x, y, z) in enumerate(spawn_points, start=1):
            x_adjusted = x + x_range * x_offset_percent_medium
            y_adjusted = y + y_range * y_offset_percent_medium
            z_adjusted = z + z_range * z_offset_percent_medium
            ax.scatter(x, y, z, color='black', s=100, edgecolors='white', linewidth=0.5)  
            ax.text(x_adjusted, y_adjusted, z_adjusted, f"{i}", color='red', fontsize=8,
                ha='center', va='center')
    else:
         for i, (x, y, z) in enumerate(spawn_points, start=1):
            x_adjusted = x + x_range * x_offset_percent_small
            y_adjusted = y + y_range * y_offset_percent_small
            z_adjusted = z + z_range * z_offset_percent_small
            ax.scatter(x, y, z, color='black', s=80, edgecolors='white', linewidth=0.5)
            ax.text(x_adjusted, y_adjusted, z_adjusted, f"{i}", color='red', fontsize=6,
                ha='center', va='center')
    ax.set_xlim(*minmax_x)
    ax.set_ylim(*minmax_y)
    ax.set_zlim(*minmax_z)
    ax.grid(True, which='both', ls="--", linewidth=0.5, color='grey')
    ax.set_axisbelow(False)
    plt.savefig(output_filename, bbox_inches='tight')
    plt.close()

def read_lump_info(file, lump_index):
    file.seek(HEADER_SIZE + lump_index * LUMP_SIZE)
    offset, length = struct.unpack('ii', file.read(LUMP_SIZE))
    return offset, length

def parse_entities(file, offset, length):
    file.seek(offset)
    entities_data = file.read(length).decode('utf-8', errors='ignore')
    global spawn_points
    spawn_points = []
    for entity in entities_data.split('}'):
        if '"classname" "info_player_deathmatch"' in entity:
            lines = entity.split('\n')
            for line in lines:
                if '"origin"' in line:
                    coords = line.split('"')[3]
                    x, y, z = map(float, coords.split(' '))
                    spawn_points.append((x, y, z))
                    break
    return spawn_points

def calculate_map_dimensions(spawn_points):
    print("...Calculating map dimensions.")
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')
    for x, y, z in spawn_points:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        min_z, max_z = min(min_z, z), max(max_z, z)
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

def process_map(pk3_name, bsp_path):
    print("...Processing spawn points.")
    global map_count
    spawn_points = None
    map_count += 1
    with open(bsp_path, 'rb') as bsp_file:
        output = []
        entities_offset, entities_length = read_lump_info(bsp_file, LUMP_ENTITIES)
        spawn_points = parse_entities(bsp_file, entities_offset, entities_length)
        if not spawn_points:
            output.append("No spawn points found in map. Skipped.")
            print("...No spawn points found in map. Skipped.")
            return
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = calculate_map_dimensions(spawn_points)
        plot_filename = f"output/img/spawn_plot_{time_short}_map_{map_count}.png"        
        generate_3d_plot(spawn_points, (min_x, max_x), (min_y, max_y), (min_z, max_z), plot_filename, map_count)
        map_name = f"{pk3_name}/{os.path.basename(bsp_path)}" if pk3_name else os.path.basename(bsp_path)
        output.append(f"Map {map_count} - {map_name}")
        output.append(f"Map Dimensions:")
        output.append("X Axis:")
        output.append(f"{min_x}")
        output.append(f"{max_x}")
        output.append("Y Axis:")
        output.append(f"{min_y}")
        output.append(f"{max_y}")
        output.append("Z Axis:")
        output.append(f"{min_z}")
        output.append(f"{max_z}")
        output.append("Spawn Points:")
        for idx, (x, y, z) in enumerate(spawn_points, start=1):
            move_left = x - min_x
            move_right = max_x - x
            move_forward = max_y - y
            move_backward = y - min_y
            move_up = max_z - z
            move_down = z - min_z
            output.append(f"Spawn Point {idx}")
            output.append(f"Spawn Position")
            output.append("X Axis")
            output.append(f"{x}")
            output.append("Y Axis")
            output.append(f"{y}")
            output.append("Z Axis")
            output.append(f"{z}")
            output.append(f"Space until void:")
            output.append(f"{move_left}")
            output.append(f"{move_right}")
            output.append(f"{move_forward}")
            output.append(f"{move_backward}")
            output.append(f"{move_up}")
            output.append(f"{move_down}")
            output.append("")
        print()
        return (output, plot_filename)

def generate_pdf(report_data, filename=f"output/vertice_output_{time_short}.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    page_width, page_height = letter
    max_image_width = page_width - 2 * inch 
    max_image_height = page_height - 2 * inch
    styles = getSampleStyleSheet()
    Story = []
    Story.append(Paragraph("Vertice (Quake III Map Boundary Analysis Tool)", styles['Heading1']))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph(f"Report generated at: {time_full}", styles['Normal']))
    Story.append(Spacer(1, 12))
    for data, plot_filename in report_data:
        if isinstance(data, list) and data:
            Story.append(Paragraph(f"{data[0]}", styles['Heading2']))
            Story.append(Spacer(1, 12))
            dimension_data = [
                ['Dimension', 'Min Value', 'Max Value'],
                ['X Axis', data[3], data[4]],
                ['Y Axis', data[6], data[7]],
                ['Z Axis', data[9], data[10]]
            ]
            dimension_table = Table(dimension_data, colWidths=[100, 100, 100], hAlign='LEFT')
            dimension_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.gray),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            Story.append(dimension_table)
            Story.append(Spacer(1, 12))
            idx = 11
            while idx + 15 < len(data): 
                spawn_details = [
                    [data[idx+1], 'Value'],
                    ['X Axis', data[idx+4]],
                    ['Y Axis', data[idx+6]],
                    ['Z Axis', data[idx+8]],
                    [data[idx+9], ''],
                    ['Left', data[idx+10]],
                    ['Right', data[idx+11]],
                    ['Forward', data[idx+12]],
                    ['Backward', data[idx+13]],
                    ['Upward', data[idx+14]],
                    ['Downward', data[idx+15]]
                ]
                sp_table = Table(spawn_details, colWidths=[150, 150], hAlign='LEFT')
                sp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey), 
                    ('BACKGROUND', (0,4), (-1,4), colors.lightgrey), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ]))
                Story.append(sp_table)
                Story.append(Spacer(1, 12))
                idx += 16 
            if plot_filename:
                image = Image(plot_filename, width=max_image_width, height=max_image_height, kind='proportional')
                Story.append(PageBreak())
                Story.append(Paragraph("Spawn points visualisation", styles['Heading1']))
                Story.append(Spacer(1, 12))
                Story.append(image)
                Story.append(PageBreak())
            else:
                Story.append(PageBreak())
                Story.append(Spacer(1, 12))
                Story.append(Paragraph("...No spawn points available for visualisation for this map.", styles['Normal']))
                Story.append(PageBreak())
    doc.build(Story)

def extract_and_process_pk3(pk3_path, temp_extract_dir="temp_maps"):
    pk3_name = os.path.basename(pk3_path)
    try:
        with zipfile.ZipFile(pk3_path, 'r') as zip_ref:
            bsp_files = [file for file in zip_ref.namelist() if file.lower().endswith(".bsp")]
            if len(bsp_files) > 1:
                print("...Extracting multiple BSP files from PK3 archive.")
            elif len(bsp_files) == 1:
                print("...Extracting BSP from PK3 archive.")
            else:
                print("...No BSP found. Skipped.")
            for bsp_file in bsp_files:
                zip_ref.extract(bsp_file, temp_extract_dir)
                bsp_path = os.path.join(temp_extract_dir, bsp_file)
                yield process_map(pk3_name, bsp_path)
    except zipfile.BadZipFile:
        print("...Error: Corrupted PK3 file. Vertice will terminate now.")
        sys.exit(1)
    finally:
        shutil.rmtree(temp_extract_dir)

def extract_and_delete_archive(archive_path, extract_to):
    pk3_found = False
    try:
        if archive_path.endswith('.zip'):
            print('...ZIP archive found. Checking for PK3...')
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                pk3_files = [f for f in zip_ref.namelist() if f.endswith('.pk3')]
                if pk3_files:
                    pk3_found = True
                    for file in pk3_files:
                        zip_ref.extract(file, extract_to)      
        elif archive_path.endswith('.7z'):
            print('...7ZIP archive found. Checking for PK3...')
            with py7zr.SevenZipFile(archive_path, mode='r') as z:
                all_files = z.getnames()
                pk3_files = [f for f in all_files if f.endswith('.pk3')]
                if pk3_files:
                    pk3_found = True
                    z.extract(targets=pk3_files, path=extract_to)
        elif archive_path.endswith('.rar'):
            print('...RAR archive found. Checking for PK3...')
            with rarfile.RarFile(archive_path) as rf:
                pk3_files = [f for f in rf.namelist() if f.endswith('.pk3')]
                if pk3_files:
                    pk3_found = True
                    for file in pk3_files:
                        rf.extract(file, extract_to)            
        if pk3_found:
            print(f"...Extracted PK3 and deleting archive: {archive_path}")
            os.remove(archive_path)
        else:
            print("...No PK3 files found in archive.")
    except Exception as e:
        print(f"...ERROR occurred while extracting {archive_path}: {e}")

def check_output_folder(input_dir='output'):
    dummy_pdf_path = os.path.join(input_dir, 'dummy_pdf.pdf')
    if os.path.exists(dummy_pdf_path):
        print('...DUMMY PDF FILE FOUND. Deleting dummy file...')
        os.remove(dummy_pdf_path)
        print('...Deleted Dummy PDF.')

def check_input_folder(input_dir='input'):
    dummy_file_path = os.path.join(input_dir, 'dummy_pk3.pk3')
    if os.path.exists(dummy_file_path):
        print("...DUMMY PK3 FILE FOUND. Deleting dummy file...")
        os.remove(dummy_file_path)
        print("...Deleted Dummy PK3.")
    input_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(('.bsp', '.pk3', '.zip', '.rar', '.7z')):
                input_files.append(os.path.join(root, file))
    if not input_files:
        check_output_folder()
        print("...NO FILES AND/OR CORRECT FILES IN INPUT FOLDER. Add .bsp files, .pk3, .zip, .rar or .7z archives to the input folder.")
        print('...TERMINATING vertice.\n')
        sys.exit(1)
    compressed_files = [file for file in input_files if file.endswith(('.7z', '.zip', '.rar'))]
    if compressed_files:
        for archive_path in compressed_files:
            extract_and_delete_archive(archive_path, input_dir)
    check_output_folder()

def temp_dir_create(input_dir='output/img'):
    os.makedirs(input_dir, exist_ok=True)

def dir_cleanup(input_dir='output/img'):
    print('...Cleaning temporary files.')
    try:
        shutil.rmtree(input_dir)
        print('...Succesfully cleaned temporary files.')
    except Exception as e:
        print(f"...FAILED to clean temporary files: {e}")

def main(input_dir='input'):
    try:
        report_data = []
        spawn_points = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.pk3') or file.endswith('.bsp'):
                    map_file = os.path.join(root, file)
                    if map_file.endswith(".pk3"):
                        for output in extract_and_process_pk3(map_file):
                            if output:
                                report_data.append(output)
                    elif map_file.endswith(".bsp"):
                        output = process_map('', map_file)
                        if output:
                            report_data.append(output)
        generate_pdf(report_data)
    except Exception as e:
        print(f"...Unexpected error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n...Operation cancelled by user.")
        sys.exit(0)

def exec_alg():
    try:
        iterate(0.5, 0.010, *"\nVertice Algorithm")
        iterate(0.5, 0.010, *"Quake III Map Boundary Analysis Tool")
        iterate(0.5, 0.010, *"Created by A Pixelated Point of View")
        iterate(0.5, 0.010, *f"Algorithm initiated at: {time_full}\n")
        time.sleep(2)
        print("...Conducting Input Check...")
        check_input_folder()
        print("...Input check passed. Running Vertice...\n")
        temp_dir_create()
        time.sleep(0.5)
        main()
        dir_cleanup()
        print("\n...Done! Check the 'OUTPUT' folder for your PDF file.")
    except KeyboardInterrupt:
        print("\n...Operation cancelled by user.")
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"...ERROR: {e.strerror} - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"...UNEXPECTED ERROR: {str(e)}")
        sys.exit(1)
    finally:
        sys.exit(0)
exec_alg()