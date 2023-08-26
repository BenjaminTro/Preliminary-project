from calculations.data_processor import read_excel_data, read_csv_data, perform_calculation
from plotting.plot_generator import plot_irr, plot_PVcalc
import matplotlib.pyplot as plt

def main():
    # Read Excel data
    input_data_PV = read_excel_data('data/PV_spec.xlsx')
    input_data_Irr = read_csv_data('data/Data_solar_irr_NOR.csv')
    print()

    # Calculate PV power production 
    PV_power = perform_calculation(input_data_PV,input_data_Irr)
    
    print("The calculated PV power production is:" + str(PV_power))
    print()

    # Print the DataFrame to the console
    print("PV Panel information:")
    print(input_data_PV)
    print()

    print("Irradiance data and other information:")
    print(input_data_Irr)
    print()

    # Generate a plot of the irradiance and PV production data (data, time resolution, color)
    plot_irr(input_data_Irr, 'D', 'purple')
    plot_PVcalc(PV_power, 'D', 'orange')


if __name__ == "__main__":
    main()


    