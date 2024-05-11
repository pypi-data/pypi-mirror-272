import openmc
import matplotlib.pyplot as plt


def _get_energy_prob(energy_dis):
    """gets the energy and probability for different openmc.stats including the
    openmc.stats.Mixutre which itself is made from openmc.stats"""

    if isinstance(energy_dis, openmc.stats.Mixture):
        stats = energy_dis.distribution
        multipliers = energy_dis.probability
    else:
        stats = [energy_dis]
        multipliers = [1.0]

    probs = []
    en = []

    for stat, multiplier in zip(stats, multipliers):

        for p in stat.p:
            probs.append(0)
            probs.append(p * multiplier)
            probs.append(0)
        for x in stat.x:
            en.append(x)
            en.append(x)
            en.append(x)

    return en, probs


def plot_gamma_emission(
    material,
    label_top: int = None,
):
    """makes a plot of the gamma energy spectra for a material. The
    material should contain unstable nuclide which undergo gamma emission
    to produce a plot. Such materials can be made manually or obtained via
    openmc deplete simulations.

    Args:
        label_top: Optionally label the n highest activity energies with
            the nuclide that generates them.

    Returns:
        Matplotlib pyplot object.
    """

    plt.clf()
    if label_top:
        energies_to_label = []
        labels = []
        possible_energies_to_label = []
        import lineid_plot

        atoms = material.get_nuclide_atoms()
        for nuc, num_atoms in atoms.items():
            dists = []
            probs = []
            source_per_atom = openmc.data.decay_photon_energy(nuc)
            if source_per_atom is not None:
                dists.append(source_per_atom)
                probs.append(num_atoms)
                combo = openmc.data.combine_distributions(dists, probs)
                for p, x in zip(combo.p, combo.x):
                    possible_energies_to_label.append((nuc, p, x))

        possible_energies_to_label = sorted(
            possible_energies_to_label, key=lambda x: x[1], reverse=True
        )[:label_top]
        for entry in possible_energies_to_label:
            energies_to_label.append(entry[2])
            labels.append(entry[0])

        probs = []
        en = []
        energy_dis = material.get_decay_photon_energy(clip_tolerance=0.0)

        en, probs = _get_energy_prob(energy_dis)

        lineid_plot.plot_line_ids(
            en,
            # material.decay_photon_energy.x,
            probs,
            # material.decay_photon_energy.p,
            energies_to_label,
            labels,
        )

    else:
        energy_dis = material.get_decay_photon_energy(clip_tolerance=0.0)

        en, probs = _get_energy_prob(energy_dis)

        # plt.scatter(energy_dis.x, energy_dis.p)
        plt.plot(en, probs)
        # print(energy_dis.p)
        # print(energy_dis.x)
    plt.xlabel("Energy [eV]")
    plt.ylabel("Activity [Bq/s]")
    return plt
