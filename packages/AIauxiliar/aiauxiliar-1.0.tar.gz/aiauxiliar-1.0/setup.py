from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='AIauxiliar',
    version=1.0,
    description='''Há muitos e muitos anos, há tantos anos quanto o número de estrelas no céu, o Paraíso Celeste
                foi palco de um terrível levante. Armados com espadas místicas e coragem divina, Querubins
                leais a Jeová travaram uma sangrenta batalha contra o arcanjo São Miguel e os anjos que o
                seguiam.
                Deus, o Senhor Supremo de Todas as Coisas, continuava imerso no profundo sono que
                caíra após ter concluído o trabalho da Criação, o descanso do Sétimo Dia. Enquanto Ele
                permanecia ausente, os arcanjos ditavam as ordens, impondo seus desígnios no Céu e na Terra.
                Sentados no topo de seus tronos de luz, cada um deles almejava alcançar a divindade.
                Concentrando todo o poder debaixo de suas asas, os poderosos arcanjos, onipotentes e
                intocáveis, utilizavam a Palavra de Deus para fazer jus à sua própria vontade. Revoltados com o
                amor do Criador para com os seres humanos, e movidos por um ciúme intenso, decidiram ir
                contra as leis do Altíssimo e destruir todo homem que caminhava sobre a Terra, acabando assim
                com parte da Criação do Divino. - A Batalha do Apocalipse, Eduardo Spohr''',
    long_description=Path('README.md').read_text(),
    author='Guilherme Menezes',
    author_email='guilherme.menezes@outlook.com',
    keywords=['AI', 'auxiliar', 'creating AI', 'creating Inteligence'],
    packages=find_packages()

)