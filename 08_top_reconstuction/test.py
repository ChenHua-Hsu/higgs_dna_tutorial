import numpy
def calculate_four_momentum(pt, eta, phi, mass):
    # Calculate px, py, pz
    px = pt * numpy.cos(phi)
    py = pt * numpy.sin(phi)
    pz = pt * numpy.sinh(eta)

    # Calculate energy
    E = numpy.sqrt(px**2 + py**2 + pz**2 + mass**2)

    return px, py, pz, E

print(calculate_four_momentum(-999,-999,-999,-999))
x,y,z,E = calculate_four_momentum(-999,-999,-999,-999)
print(numpy.sqrt(E**2 - x**2 - y**2 - z**2))