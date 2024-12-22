import numpy as np
import matplotlib.pyplot as plt

#beam length
beam_length = 10
#point load
point_loads = np.array([[3,20],[7,30]])
#udl load
udls=np.array([[2,6,10]])

def reaction_force_calculation(beam_lenght,point_loads,udsl):
    positions = point_loads[:,0]
    loads = point_loads[:,1]

    total_vertical_force = np.sum(loads)
    total_moment = np.sum(loads*positions)

    for start,end,intensity in udls:
        length = end-start
        udl_load = intensity * length
        udl_moment = udl_load * (start+length/2 )
        total_vertical_force += udl_load
        total_moment += udl_moment

    R_B = total_moment/beam_lenght
    R_A = total_vertical_force - R_B

    return R_A,R_B


reaction_force_a, reaction_force_b = reaction_force_calculation(beam_length,point_loads,udls)
print(reaction_force_a,reaction_force_b)

def shear_force(beam_length,point_loads,udl_loads,reaction_a):
    x = np.linspace(0,beam_length,1000)
    sf = np.zeros_like(x)

    sf+=reaction_a

    for position,loads in point_loads:
        sf[x >= position] -= loads

    for start,end,intensity in udls:
        sf += np.where((x>=start) & (x<=end), -intensity * (x-start),0)
        sf[x>end] -= intensity * (end - start)

    return x,sf

x,sf = shear_force(beam_length,point_loads,udls,reaction_force_a)
# print(x)
# print(sf)

def bending_moment(beam_length,point_loads,udl_loads,reaction_a):
    x = np.linspace(0, beam_length, 1000)
    bm = np.zeros_like(x)

    bm += reaction_a * x

    for position, loads in point_loads:
        bm += np.where(x >= position, -loads * (x-position), 0)
    for start, end, intensity in udl_loads:
        bm += np.where(
            (x >= start) & (x <= end),
            -intensity * ((x - start) ** 2) / 2,
            0,
        )
        bm += np.where(
            x > end,
            -intensity * (end - start) * (x - (start + (end - start) / 2)),
            0
        )
    return x, bm

x,bm = bending_moment(beam_length,point_loads,udls,reaction_force_a)
# print(x)
# print(bm)

#shear force diagram
x_sf,sf = shear_force(beam_length,point_loads,udls,reaction_force_a)
plt.figure(figsize=(10, 5))
plt.plot(x_sf, sf, label="Shear Force(KN)", color="blue")
plt.axhline(0, color="black", linestyle="--")
plt.fill_between(x_sf, 0, sf, where=sf > 0, color="blue", alpha=0.3)
plt.fill_between(x_sf, 0, sf, where=sf < 0, color="red", alpha=0.3)
plt.title("Shear Force Diagram")
plt.xlabel("Beam Length (m)")
plt.ylabel("Shear Force (kN)")
plt.grid()
plt.legend()
plt.show()

#Bending diagram
x_bm,bm = bending_moment(beam_length,point_loads,udls,reaction_force_a)
plt.figure(figsize=(10, 5))
plt.plot(x_bm, bm, label="Bending Moment (KN·m)", color="green")
plt.axhline(0, color="black", linestyle="--")
plt.fill_between(x_bm, 0, bm, where=bm > 0, color="blue", alpha=0.3)
plt.fill_between(x_bm, 0, bm, where=bm < 0, color="red", alpha=0.3)
plt.title("Bending Moment Diagram")
plt.xlabel("Beam Length (m)")
plt.ylabel("Bending Moment (kN·m)")
plt.grid()
plt.legend()
plt.show()