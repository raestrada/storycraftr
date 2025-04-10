import click
from storycraftr.cmd.paper.publish import publish
from storycraftr.cmd.paper.iterate import iterate
from storycraftr.cmd.paper.generate_section import generate
from storycraftr.cmd.paper.organize_lit import organize_lit
from storycraftr.cmd.paper.outline_sections import outline_sections
from storycraftr.cmd.paper.references import references
from storycraftr.cmd.paper.abstract import abstract


@click.group()
def paper():
    """PaperCraftr commands for academic paper writing."""
    pass


paper.add_command(publish)
paper.add_command(iterate)
paper.add_command(generate)
paper.add_command(organize_lit)
paper.add_command(outline_sections)
paper.add_command(references)
paper.add_command(abstract)
