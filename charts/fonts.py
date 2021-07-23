
import matplotlib.pyplot as plt
import seaborn as sns


def fonts():
	sns.set_style("white")
	sns.set_context("paper")

	# Start a dictionary for LaTeX properties.
	props = {"text.usetex": True}

	# If LaTeX is enabled, then we have to set the rcparams to allow the
	# default LaTeX text to be the font we want.
	props.update({
		"font.family": "serif",
		"font.serif": "New Century Schoolbook"
	})

	# If we turn LaTeX rendering on, then everything is sent to the TeX
	# rendering engine. If we do that, we have to import specific packages
	# to allow LaTeX to render fonts properly.
	plt.rcParams.update(props)
