import matplotlib.pyplot as plt

class DepthDataVisualizer:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Depth')
        plt.title('3D Depth Data')

    def plot_data(self, data):
        xs = [point[0] for point in data]
        ys = [point[1] for point in data]
        zs = [point[2] for point in data]
        colors = zs

        # Z軸を逆転
        self.ax.set_zlim(max(zs), min(zs))

        self.ax.scatter(xs, ys, zs, c=colors, cmap='viridis')
        self.fig.colorbar(plt.cm.ScalarMappable(cmap='viridis'), ax=self.ax, label='Depth')

    def show(self):
        plt.show()
