import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def main():
    st.title("Underground Pipe and Water Table Visualization")
    
    # Set up the sidebar for user inputs
    st.sidebar.header("Depth Parameters (meters)")
    
    # User inputs for depths
    water_table_depth = st.sidebar.slider("Water Table Depth", 1.0, 10.0, 5.0, 0.1)
    pipe_top_depth = st.sidebar.slider("Pipe Top Depth", 0.5, 9.0, 3.0, 0.1)
    pipe_diameter = st.sidebar.slider("Pipe Diameter", 0.1, 2.0, 0.5, 0.1)
    
    # Derived measurements
    pipe_middle_depth = pipe_top_depth + pipe_diameter/2
    pipe_bottom_depth = pipe_top_depth + pipe_diameter
    
    # Gap between water table and pipe top
    water_pipe_gap = water_table_depth - pipe_top_depth if water_table_depth > pipe_top_depth else 0
    
    # Create the visualization
    create_visualization(water_table_depth, pipe_top_depth, pipe_middle_depth, 
                         pipe_bottom_depth, pipe_diameter, water_pipe_gap)

def create_visualization(water_table_depth, pipe_top_depth, pipe_middle_depth, 
                         pipe_bottom_depth, pipe_diameter, water_pipe_gap):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Ground surface parameters
    ground_width = 10
    max_depth = 12
    
    # Draw ground surface
    ground_x = np.linspace(0, ground_width, 500)
    ground_surface = 0.1 * np.sin(ground_x * 2) + 0.05 * np.random.randn(len(ground_x))
    ax.plot(ground_x, ground_surface, 'k-', linewidth=2)
    ax.fill_between(ground_x, ground_surface, max_depth, color='sienna', alpha=0.5)
    
    # Draw water table
    ax.axhline(y=water_table_depth, color='royalblue', linestyle='-', linewidth=2)
    ax.fill_between(ground_x, water_table_depth, max_depth, color='royalblue', alpha=0.3)
    
    # Draw pipe
    pipe_x = ground_width / 2
    pipe_width = ground_width / 4
    pipe_left = pipe_x - pipe_width/2
    pipe_right = pipe_x + pipe_width/2
    
    # Draw pipe
    pipe_rect = plt.Rectangle((pipe_left, pipe_top_depth), pipe_width, pipe_diameter, 
                             facecolor='gray', edgecolor='black', alpha=0.8)
    ax.add_patch(pipe_rect)
    
    # Add depth arrows
    arrow_props = dict(arrowstyle='<->', color='black', linewidth=1.5)
    
    # Water table depth arrow
    ax.annotate('', xy=(0.5, 0), xytext=(0.5, water_table_depth),
                arrowprops=arrow_props)
    ax.text(0.6, water_table_depth/2, f'Water Table Depth\n{water_table_depth:.1f} m', 
           ha='left', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Pipe top depth arrow
    ax.annotate('', xy=(pipe_left - 0.5, 0), xytext=(pipe_left - 0.5, pipe_top_depth),
                arrowprops=arrow_props)
    ax.text(pipe_left - 0.6, pipe_top_depth/2, f'Pipe Top Depth\n{pipe_top_depth:.1f} m', 
           ha='right', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Pipe middle depth arrow
    ax.annotate('', xy=(pipe_left - 0.5, 0), xytext=(pipe_left - 0.5, pipe_middle_depth),
                arrowprops=arrow_props)
    ax.text(pipe_left - 0.6, pipe_middle_depth, f'Pipe Middle\n{pipe_middle_depth:.1f} m', 
           ha='right', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Pipe bottom depth arrow
    ax.annotate('', xy=(pipe_left - 0.5, 0), xytext=(pipe_left - 0.5, pipe_bottom_depth),
                arrowprops=arrow_props)
    ax.text(pipe_left - 0.6, pipe_bottom_depth, f'Pipe Bottom\n{pipe_bottom_depth:.1f} m', 
           ha='right', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Gap between water table and pipe (if pipe is above water table)
    if water_pipe_gap > 0:
        ax.annotate('', xy=(pipe_right + 0.5, pipe_top_depth), 
                   xytext=(pipe_right + 0.5, water_table_depth),
                   arrowprops=arrow_props)
        ax.text(pipe_right + 0.6, pipe_top_depth + water_pipe_gap/2, 
               f'Gap\n{water_pipe_gap:.1f} m', 
               ha='left', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Set axis properties
    ax.set_xlim(0, ground_width)
    ax.set_ylim(max_depth, -1)  # Invert y-axis to show depth increasing downward
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Ground Surface with Underground Pipe and Water Table')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='k', lw=2, label='Ground Surface'),
        Line2D([0], [0], color='royalblue', lw=2, label='Water Table'),
        Patch(facecolor='gray', edgecolor='black', label='Pipe', alpha=0.8)
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Display the figure in Streamlit
    st.pyplot(fig)
    
    # Display additional information
    st.subheader("Measurement Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Water Table Depth", f"{water_table_depth:.1f} m")
        st.metric("Pipe Top Depth", f"{pipe_top_depth:.1f} m")
    with col2:
        st.metric("Pipe Middle Depth", f"{pipe_middle_depth:.1f} m")
        st.metric("Pipe Bottom Depth", f"{pipe_bottom_depth:.1f} m")
    with col3:
        st.metric("Pipe Diameter", f"{pipe_diameter:.1f} m")
        if water_pipe_gap > 0:
            st.metric("Water-Pipe Gap", f"{water_pipe_gap:.1f} m")
        else:
            st.metric("Water-Pipe Gap", "Pipe is below water table")

if __name__ == "__main__":
    main()
