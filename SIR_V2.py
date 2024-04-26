import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

import customtkinter as ctk

# SEIRS Model with Vaccination
def model_seirs_vaccination(y, t, beta, sigma, gamma, vaccination_rate):
    S, E, I, R = y
    dSdt = -beta * S * I - vaccination_rate * S
    dEdt = beta * S * I - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I + vaccination_rate * S
    return [dSdt, dEdt, dIdt, dRdt]

# Function to solve the system of differential equations with odeint
def solve_model(beta, sigma, gamma, vaccination_rate, S0, E0, I0, R0, t):
    y = odeint(model_seirs_vaccination, [S0, E0, I0, R0], t, args=(beta, sigma, gamma, vaccination_rate))
    S, E, I, R = y.T
    return S, E, I, R

# Function to update the fields based on the selected model
def update_fields(event):
    selected_model = model_var.get()
    if selected_model == "SIR":
        entry_E0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for E0
        entry_sigma.configure(state='normal', fg_color='white')  # Enable the entry for sigma
        entry_R0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for R0
    elif selected_model == "SIS":
        entry_E0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for E0
        entry_sigma.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for sigma
        entry_R0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for R0
    elif selected_model == "SIRS":
        entry_E0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for E0
        entry_sigma.configure(state='normal', fg_color='white')  # Enable the entry for sigma
        entry_R0.configure(state='normal', fg_color='white')  # Enable the entry for R0
    elif selected_model == "SEIR":
        entry_E0.configure(state='normal', fg_color='white')  # Enable the entry for E0
        entry_sigma.configure(state='normal', fg_color='white')  # Enable the entry for sigma
        entry_R0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for R0
    elif selected_model == "SEIS":
        entry_E0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for E0
        entry_sigma.configure(state='normal', fg_color='white')  # Enable the entry for sigma
        entry_R0.configure(state='disabled', fg_color='#dddddd')  # Disable the entry for R0
    elif selected_model == "SEIRS":
        entry_E0.configure(state='normal', fg_color='white')  # Enable the entry for E0
        entry_sigma.configure(state='normal', fg_color='white')  # Enable the entry for sigma
        entry_R0.configure(state='normal', fg_color='white')  # Enable the entry for R0

def update_plot():
    # Retrieve the parameter values from the Entry fields.
    beta = float(entry_beta.get())
    sigma = float(entry_sigma.get())
    gamma = float(entry_gamma.get())
    vaccination_rate = float(entry_vaccination.get())
    S0 = float(entry_S0.get())
    I0 = float(entry_I0.get())

    # Define the time vector 't'
    t = np.linspace(0, 200, 1000)
    
    # Initialize variables specific to each model
    E0 = 0
    R0 = 0

    # Replace appropriate values with zero based on the selected mode
    model_type = model_var.get()
    if model_type == "SIR":
        E0 = 0
        R0 = 0
    elif model_type == "SIS":
        E0 = 0
        sigma = 0
        R0 = 0
    elif model_type == "SIRS":
        E0 = 0
        sigma = 0
    elif model_type == "SEIR":
        R0 = 0
    elif model_type == "SEIS":
        R0 = 0

    # Solve the model
    S, E, I, R = solve_model(beta, sigma, gamma, vaccination_rate, S0, E0, I0, R0, t)

    # Update the graph data
    ax.plot(t, S, label='Susceptible', color='blue')
    if model_type != "SIR" and model_type != "SIS" and model_type != "SEIR" and model_type != "SIRS":
        ax.plot(t, E, label='Exposed', color='orange')
    ax.plot(t, I, label='Infected', color='red')
    ax.plot(t, R, label='Recovered', color='green')
    ax.set_title('Model SEIRS with Vaccination')
    ax.set_xlabel('Time(D)')
    ax.set_ylabel('Proportion of the population')
    ax.legend()
    canvas.draw()

# Function to display contextual help
def show_help(text):
    messagebox.showinfo("Aide", text)

# Create an information button with an information icon
def create_info_button(master, help_text):
    info_button = ctk.CTkButton(master, text="?", width=5, corner_radius=10, command=lambda: show_help(help_text))
    return info_button


# Create a Tkinter window
root = Tk()
root.title('Model SEIRS with Vaccination')

root.config(bg="#B7C9F2")  

# Create a custom dropdown menu
model_var = StringVar(root)
model_var.set("SEIRS")  # Default value
models = ["SIR", "SEIR", "SIS", "SIRS", "SEIS", "SEIRS"]
model_menu = ctk.CTkOptionMenu(root, values=models, command=update_fields, variable=model_var)
model_menu.grid(row=0, column=0, columnspan=3, pady=10)

# Create custom Entry fields for parameters
ctk_entry_style = {
    "corner_radius": 10,  # Corner radius
    "border_width": 2,    # Border width
    "font": ("Arial", 12),  # Font
}

entry_beta = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2")
entry_beta.grid(row=1, column=1, pady=5)
info_beta = create_info_button(root, "The rate of transmission controls the speed of disease transmission")
info_beta.grid(row=1, column=2, pady=5)

entry_sigma = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2",)
entry_sigma.grid(row=2, column=1,pady=5)
info_sigma = create_info_button(root, "Contact rate is the rate at which an exposed person becomes infected")
info_sigma.grid(row=2, column=2,pady=5)
entry_gamma = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2")
entry_gamma.grid(row=3, column=1,pady=5)
info_gamma = create_info_button(root, "The recovery rate is the rate at which infected individuals recover from the disease")
info_gamma.grid(row=3, column=2,pady=5)

entry_vaccination = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2")
entry_vaccination.grid(row=4, column=1,pady=5)
info_vaccination = create_info_button(root, "The vaccination rate is the percentage of the population that is vaccinated per unit of time")
info_vaccination.grid(row=4, column=2,pady=5)

entry_S0 = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2")
entry_S0.grid(row=5, column=1,pady=5)
info_S0 = create_info_button(root, "The initial proportion of susceptible is the percentage of the population that is likely to be infected at the beginning of the simulation")
info_S0.grid(row=5, column=2,pady=5)

entry_E0 = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2")
entry_E0.grid(row=6, column=1,pady=5)
info_E0 = create_info_button(root, "The initial proportion of exposures is the percentage of the population that is exposed to the disease at the beginning of the simulation")
info_E0.grid(row=6, column=2,pady=5)

entry_I0 = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2")
entry_I0.grid(row=7, column=1,pady=5)
info_I0 = create_info_button(root, "The initial proportion of infected is the percentage of the population that is infected at the beginning of the simulation")
info_I0.grid(row=7, column=2,pady=5)

entry_R0 = ctk.CTkEntry(root, **ctk_entry_style, bg_color="#B7C9F2")
entry_R0.grid(row=8, column=1,pady=5)
info_R0 = create_info_button(root, "The initial proportion of recovered is the percentage of the population that is recovered from the disease at the beginning of the simulation")
info_R0.grid(row=8, column=2,pady=5)

# Create labels for parameter descriptions
label_style = {
    "font": ("Arial", 12),  # Police de caractères
    "background":"#B7C9F2",
}

Label(root, text='Transmission rate (beta):', **label_style, ).grid(row=1, column=0,pady=5)
Label(root, text='Contact rate (sigma):', **label_style).grid(row=2, column=0,pady=5)
Label(root, text='Recovery rate (gamma):', **label_style).grid(row=3, column=0,pady=5)
Label(root, text='Vaccination rate:', **label_style).grid(row=4, column=0,pady=5)
Label(root, text='Initial proportion of susceptibles (S0):', **label_style).grid(row=5, column=0,pady=5)
Label(root, text="Initial proportion of exposed (E0):", **label_style).grid(row=6, column=0,pady=5)
Label(root, text="Initial proportion of infected (I0):", **label_style).grid(row=7, column=0,pady=5)
Label(root, text='Initial proportion of recovered (R0):', **label_style).grid(row=8, column=0,pady=5)


# Create a custom "Update Chart" button
update_button = ctk.CTkButton(root, text="Update Chart", command=update_plot, corner_radius=10)
update_button.grid(row=9, column=0, columnspan=3,pady=10)

# Create the initial chart
fig, ax = plt.subplots(figsize=(8, 3.7))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=10, column=0, columnspan=3)

# Default model parameters
default_params = {'beta': 0.4, 'sigma': 0.2, 'gamma': 0.1, 'vaccination_rate': 0.05, 'S0': 0.99, 'E0': 0.0, 'I0': 0.01, 'R0': 0.0}

# Fill the Entry fields with default parameters
entry_beta.insert(0, default_params['beta'])
entry_sigma.insert(0, default_params['sigma'])
entry_gamma.insert(0, default_params['gamma'])
entry_vaccination.insert(0, default_params['vaccination_rate'])
entry_S0.insert(0, default_params['S0'])
entry_E0.insert(0, default_params['E0'])
entry_I0.insert(0, default_params['I0'])
entry_R0.insert(0, default_params['R0'])

# Update the initial chart with default parameters
update_plot()

# Start the main Tkinter loop
root.mainloop()
