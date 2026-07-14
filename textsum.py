import click
from summarizer import input_utils
from summarizer import extractive
from summarizer import abstractive


@click.command()
@click.argument('input', required=True)
@click.option('-m', '--mode', type=click.Choice(['extractive', 'abstractive']), default='extractive', help='Summarization mode')
@click.option('-l', '--lines', type=int, default=5, help='Number of sentences in summary')
@click.option('-o', '--output', type=click.Path(), help='Write to file instead of stdout')
def main(input, mode, lines, output):
    text = input_utils.read_input(input)
    if mode == 'extractive':
        result = extractive.summarize(text, num_lines=lines)
    else:
        result = abstractive.summarize(text, num_lines=lines)

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result + '\n')
    else:
        click.echo(result)


if __name__ == '__main__':
    main()
