import click
import unidecode
import gnureadline

_ = gnureadline.__file__


def to_snake_case(text):
    text = unidecode.unidecode(text)
    text = ''.join(['_' if not char.isalnum() else char for char in text])
    text = text.lower()
    return text


class CustomHelpCommand(click.Command):
    def format_usage(self, ctx, formatter):
        usage_prefix = 'Normalizador de nome de pastas [Opções]'
        formatter.write_usage('', usage_prefix, prefix='Modo de usar:')

    def format_options(self, ctx, formatter):
        options = []
        for param in self.get_params(ctx):
            help_record = param.get_help_record(ctx)
            if help_record:
                if param.opts == ['--text', '-t']:
                    options.append(('-t, --text TEXT', help_record[1]))
                elif '--help' in param.opts:
                    options.append(('-h, --help', 'Mostra ajuda personalizada para o prompt.'))
                else:
                    options.append(help_record)
        if options:
            with formatter.section("Options"):
                formatter.write_dl(options)


text_label = "Insira o texto que deseja normalizar para a criação de uma pasta"


@click.command(cls=CustomHelpCommand, context_settings={"help_option_names": ['-h', '--help']})
@click.option('-t', '--text', prompt=text_label, help=text_label)
def cli(text):
    """Esta aplicação CLI recebe um texto converte para um nome normalizado para a criação de uma pasta."""
    result = to_snake_case(text)
    click.echo(result)


if __name__ == '__main__':
    cli()
