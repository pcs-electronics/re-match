#!/usr/bin/env python3

import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
import re
import skrf as rf

def parse_touchstone(data):
    """Parse Touchstone data into a structured format and convert to S,RI format."""
    lines = data.strip().split('\n')
    
    # Skip comment lines
    header_line = None
    for line in lines:
        if line.startswith('#'):
            header_line = line
            break
    
    if not header_line:
        raise ValueError("Invalid Touchstone format: No header line found.")
    
    # Parse header to determine format
    header_parts = header_line.split()
    if len(header_parts) < 4:
        raise ValueError("Invalid Touchstone format: Header line is too short.")
    
    # Determine the format (S,RI, S,MA, S,DB, or Z,RI)
    format_type = None
    if 'S' in header_parts and 'RI' in header_parts:
        format_type = 'S_RI'
    elif 'S' in header_parts and 'MA' in header_parts:
        format_type = 'S_MA'
    elif 'S' in header_parts and 'DB' in header_parts:
        format_type = 'S_DB'
    elif 'Z' in header_parts and 'RI' in header_parts:
        format_type = 'Z_RI'
    else:
        raise ValueError("Unsupported Touchstone format: Must be S,RI, S,MA, S,DB, or Z,RI.")
    
    # Parse data lines and convert to S,RI format
    frequencies = []
    s_ri_values = []
    
    for line in lines:
        if not line.startswith('!') and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 3:
                try:
                    freq = float(parts[0])
                    val1 = float(parts[1])
                    val2 = float(parts[2])
                    
                    # Convert to S,RI format
                    if format_type == 'S_RI':
                        # Already in S,RI format
                        s_real = val1
                        s_imag = val2
                    elif format_type == 'S_MA':
                        # Convert from magnitude and angle to real and imaginary
                        magnitude = val1
                        angle_rad = np.radians(val2)
                        s_real = magnitude * np.cos(angle_rad)
                        s_imag = magnitude * np.sin(angle_rad)
                    elif format_type == 'S_DB':
                        # Convert from dB to real and imaginary
                        magnitude = 10 ** (val1 / 20)
                        angle_rad = np.radians(val2)
                        s_real = magnitude * np.cos(angle_rad)
                        s_imag = magnitude * np.sin(angle_rad)
                    elif format_type == 'Z_RI':
                        # Convert from Z,RI to S,RI format
                        # Z = R + jX, S = (Z - Z0) / (Z + Z0)
                        z0 = 50  # Reference impedance
                        z = val1 + 1j * val2
                        s = (z - z0) / (z + z0)
                        s_real = s.real
                        s_imag = s.imag
                    
                    frequencies.append(freq)
                    s_ri_values.append((s_real, s_imag))
                except ValueError:
                    continue
    
    return {
        'format': format_type,
        'frequencies': frequencies,
        's_ri_values': s_ri_values
    }

def read_input(input_file=None):
    """Read input from stdin or a file."""
    if input_file:
        try:
            with open(input_file, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        return sys.stdin.read()

def calculate_swr(s_ri_values):
    """Calculate SWR from S,RI values."""
    swr_values = []
    for s_real, s_imag in s_ri_values:
        gamma = np.abs(s_imag + 1j * s_real)
        swr = (1 + gamma) / (1 - gamma)
        swr_values.append(swr)
    return swr_values

def plot_swr10(frequencies, s_ri_values, output_file):
    """Plot SWR up to 10."""
    swr_values = calculate_swr(s_ri_values)
    
    plt.figure()
    plt.plot(frequencies, swr_values)
    plt.ylim(1, 10)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('SWR')
    plt.title('SWR to 10')
    plt.grid(True)
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def plot_swr2(frequencies, s_ri_values, output_file):
    """Plot SWR up to 2."""
    swr_values = calculate_swr(s_ri_values)
    
    plt.figure()
    plt.plot(frequencies, swr_values)
    plt.ylim(1, 2)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('SWR')
    plt.title('SWR to 2')
    plt.grid(True)
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def plot_s11(frequencies, s_ri_values, output_file):
    """Plot S11 parameter in dB."""
    s11_magnitude_db = [20 * np.log10(np.abs(s_real + 1j * s_imag)) for s_real, s_imag in s_ri_values]
    
    plt.figure()
    plt.plot(frequencies, s11_magnitude_db)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('|S11| (dB)')
    plt.title('S11 Magnitude (dB)')
    plt.grid(True)
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def plot_rx1000(frequencies, s_ri_values, output_file):
    """Plot RX up to 1000."""
    # Calculate impedance from S-parameters
    z0 = 50  # Reference impedance
    r_values = []
    x_values = []
    
    for s_real, s_imag in s_ri_values:
        s = s_real + 1j * s_imag
        z = z0 * (1 + s) / (1 - s)
        r_values.append(z.real)
        x_values.append(z.imag)
    
    plt.figure()
    plt.plot(frequencies, r_values, label='Resistance')
    plt.plot(frequencies, x_values, label='Reactance')
    plt.ylim(-1000, 1000)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Impedance')
    plt.title('RX to 1000')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def plot_rx100(frequencies, s_ri_values, output_file):
    """Plot RX up to 100."""
    # Calculate impedance from S-parameters
    z0 = 50  # Reference impedance
    r_values = []
    x_values = []
    
    for s_real, s_imag in s_ri_values:
        s = s_real + 1j * s_imag
        z = z0 * (1 + s) / (1 - s)
        r_values.append(z.real)
        x_values.append(z.imag)
    
    plt.figure()
    plt.plot(frequencies, r_values, label='Resistance')
    plt.plot(frequencies, x_values, label='Reactance')
    plt.ylim(-100, 100)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Impedance')
    plt.title('RX to 100')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def plot_smith(frequencies, s_ri_values, output_file):
    """Plot Smith chart using skrf."""
    # Convert S,RI to complex S-parameters
    s_parameters = [s_real + 1j * s_imag for s_real, s_imag in s_ri_values]
    
    freq = rf.Frequency(frequencies[0], frequencies[-1], len(frequencies), 'MHz')
    network = rf.Network(frequency=freq, s=s_parameters, z0=50)
    
    plt.figure()
    network.plot_s_smith(lw=2, draw_labels=True, chart_type='z',
                         color='r',
                         markersize=3,
                         marker='o',
                         markevery=[0, len(frequencies)//2, -1],
                         mfc='black',
                         mec='blue')
    plt.title('Smith Chart')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Plot saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Plot Touchstone data from stdin or a file.",
        epilog="Example: python tt-plot.py --type swr10 --output plot.png data.s1p"
    )
    
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        choices=['swr10', 'swr2', 's11', 'rx1000', 'rx100', 'smith'],
        help='Type of plot to generate'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output file for the plot'
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        nargs='?',
        help='Input file in Touchstone format (.s1p)'
    )
    
    args = parser.parse_args()
    
    # Read input
    data = read_input(args.input_file)
    
    # Parse Touchstone data
    try:
        touchstone_data = parse_touchstone(data)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate plot based on type
    if args.type == 'swr10':
        plot_swr10(touchstone_data['frequencies'], touchstone_data['s_ri_values'], args.output)
    elif args.type == 'swr2':
        plot_swr2(touchstone_data['frequencies'], touchstone_data['s_ri_values'], args.output)
    elif args.type == 's11':
        plot_s11(touchstone_data['frequencies'], touchstone_data['s_ri_values'], args.output)
    elif args.type == 'rx1000':
        plot_rx1000(touchstone_data['frequencies'], touchstone_data['s_ri_values'], args.output)
    elif args.type == 'rx100':
        plot_rx100(touchstone_data['frequencies'], touchstone_data['s_ri_values'], args.output)
    elif args.type == 'smith':
        plot_smith(touchstone_data['frequencies'], touchstone_data['s_ri_values'], args.output)

if __name__ == '__main__':
    main()