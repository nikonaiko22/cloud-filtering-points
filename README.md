Intelligent Point Cloud Filter (X, Y, Z)

Description:
	
This desktop application, developed in Python with Tkinter, allows you to import, visualize, and filter 2D point clouds (X, Y, Z) typically obtained from laser scanners or total stations. The tool helps clean data by removing points outside a user-defined rectangular area and supports flexible input/output formats

Main Features

	✅ Import .txt or .csv files containing point cloud data.

	✅ Flexible input formats: Choose among the following formats when importing:

		PNEZD (Point, Northing, Easting, Elevation, Description)

		PENZD (Point, Easting, Northing, Elevation, Description)

		ENZD (Easting, Northing, Elevation, Description)

		NEZD (Northing, Easting, Elevation, Description)

	✅ Select field separator when importing or exporting: comma, semicolon, or space. (New)

	✅ Automatic duplicate detection with option to remove them. (New)

	✅ Optional support for a description field per point. (New)

	📈 Interactive 2D visualization of the point cloud on the XY plane using Matplotlib.

	🖱️ User-defined boundary filters: Enter Xmin, Xmax, Ymin, Ymax to define a rectangular area of interest.

	🧹 Filter operation keeps only points inside the defined rectangle.

	💾 Export filtered points with chosen format and delimiter. (Updated)

	✨ Clean, user-friendly interface designed for non-technical users.

Requirements

	Python 3.7 or higher

Libraries:

 	 -tkinter (included with standard Python)
  
 	 -pandas
  
 	 -matplotlib

Install dependencies with:

 	pip install pandas matplotlib

How It Works:

	1)Run the Python script.

	2)Click "Import TXT" to load a .txt or .csv file.

	3)Choose the data format and delimiter (comma, semicolon, space) when prompted.

	4)The file can contain:

		3 columns (X, Y, Z)

		Or 4–5 columns if using full PNEZD/PENZD formats

	5)Points are displayed in a 2D graph on the XY plane.

	6)Enter boundary values for Xmin, Xmax, Ymin, and Ymax.

	7)Click "Filter" to show only points within the rectangle.

	8)Optionally, click "Export TXT" to save the filtered cloud using your preferred format and delimiter.

🧾 Supported Input Formats
   Each line can contain:

	X: Easting (float)

	Y: Northing (float)

	Z: Elevation (float)

	[Optional] Description: Text label

	[Optional] Point number    

Delimiters supported: space, comma, semicolon

Examples:

	3000.10,70000.00,120.5
	3001.50,70001.20,121.0
	3003.00,70002.10,122.3
 
	Or
 
 	12  70000.00  3000.10  120.5  B1
	13  70001.20  3001.50  121.0  B2
	14  70002.10  3003.00  122.3  B3


