import discord
from discord.ext import commands
from bot_logic import gen_pass

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)
    
    if not message.content.startswith('$'):
        await message.channel.send(message.content)

@bot.command()
async def hello(ctx):
    await ctx.send("Hi!")

@bot.command()
async def bye(ctx):
    await ctx.send("\U0001f642")

@bot.command(name='pass')
async def password(ctx):
    await ctx.send(f"se genero correctamente su contraseña, su contraseña es:{gen_pass(10)}")

@bot.command(name='bot')
async def _bot(ctx):
    await ctx.send('yo que? quieres pelea? ')

@bot.command()
async def menu(ctx):
    embed = discord.Embed(
        title="\U0001f4dc Menú de Comandos",
        description="Aquí están todos los comandos disponibles:",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="\U0001f44b $hello",
        value="El bot te saluda con un 'Hi!'",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f44b $bye",
        value="El bot se despide con un emoji",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f512 $pass",
        value="Genera una contraseña aleatoria segura",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f916 $bot",
        value="El bot te reta a pelear",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f3ae $recomendar",
        value="Recomienda juegos según el género que elijas (FPS, Battle Royale, Survival, Ritmo)",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f4dc $menu",
        value="Muestra este menú de comandos",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f4ac Repetidor",
        value="Escribe cualquier mensaje sin $ y el bot lo repetirá",
        inline=False
    )
    
    embed.set_footer(text="Usa el prefijo $ antes de cada comando")
    
    await ctx.send(embed=embed)

@bot.command()
async def recomendar(ctx):
    juegos = {
        '\U0001f3af': {
            'genero': 'FPS',
            'juegos': [
                {
                    'nombre': 'Counter-Strike', 
                    'desc': 'Shooter táctico competitivo 5v5 donde terroristas y antiterroristas luchan en partidas estratégicas',
                    'link': 'https://store.steampowered.com/app/730/CounterStrike_2/'
                },
                {
                    'nombre': 'Valorant', 
                    'desc': 'FPS táctico con agentes únicos y habilidades especiales en combates 5v5',
                    'link': 'https://playvalorant.com/es-es/download/'
                }
            ]
        },
        '\u2694\ufe0f': {
            'genero': 'Battle Royale',
            'juegos': [
                {
                    'nombre': 'Fortnite', 
                    'desc': 'Battle royale con construcción donde 100 jugadores luchan hasta quedar uno',
                    'link': 'https://www.fortnite.com/download'
                },
                {
                    'nombre': 'Warzone', 
                    'desc': 'Battle royale ambientado en Call of Duty con acción realista y equipos tácticos',
                    'link': 'https://www.callofduty.com/es/warzone'
                },
                {
                    'nombre': 'PUBG', 
                    'desc': 'El battle royale original con combate realista en mapas masivos',
                    'link': 'https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/'
                }
            ]
        },
        '\U0001f3d5\ufe0f': {
            'genero': 'Survival',
            'juegos': [
                {
                    'nombre': 'ARK: Survival Evolved', 
                    'desc': 'Sobrevive en una isla prehistórica domando dinosaurios y construyendo bases',
                    'link': 'https://store.steampowered.com/app/346110/ARK_Survival_Evolved/'
                },
                {
                    'nombre': 'Minecraft', 
                    'desc': 'Construye, explora y sobrevive en un mundo de bloques infinito',
                    'link': 'https://www.minecraft.net/es-es/download'
                },
                {
                    'nombre': 'The Forest', 
                    'desc': 'Survival horror donde debes sobrevivir en una isla llena de caníbales mutantes',
                    'link': 'https://store.steampowered.com/app/242760/The_Forest/'
                }
            ]
        },
        '\U0001f3b5': {
            'genero': 'Ritmo',
            'juegos': [
                {
                    'nombre': 'osu!', 
                    'desc': 'Juego de ritmo donde clickeas círculos siguiendo el beat de la música con múltiples modos de juego',
                    'link': 'https://osu.ppy.sh/home/download'
                },
                {
                    'nombre': 'Friday Night Funkin', 
                    'desc': 'Juego de ritmo estilo rap battle donde compites en duelos musicales presionando flechas al ritmo',
                    'link': 'https://ninja-muffin24.itch.io/funkin'
                },
                {
                    'nombre': 'Project Sekai', 
                    'desc': 'Juego de ritmo con personajes de Vocaloid donde tocas canciones y coleccionas cartas de personajes',
                    'link': 'https://play.google.com/store/apps/details?id=com.sega.pjsekai'
                }
            ]
        }
    }
    
    embed = discord.Embed(
        title="\U0001f3ae Recomendador de Juegos",
        description="Reacciona con el emoji del género que te interese:",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="\U0001f3af FPS", value="Juegos de disparos en primera persona", inline=False)
    embed.add_field(name="\u2694\ufe0f Battle Royale", value="Combate hasta ser el último en pie", inline=False)
    embed.add_field(name="\U0001f3d5\ufe0f Survival", value="Supervivencia y construcción", inline=False)
    embed.add_field(name="\U0001f3b5 Ritmo", value="Juegos musicales y de ritmo", inline=False)
    
    mensaje = await ctx.send(embed=embed)
    
    for emoji in juegos.keys():
        await mensaje.add_reaction(emoji)
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in juegos.keys() and reaction.message.id == mensaje.id
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        seleccion = juegos[str(reaction.emoji)]
        
        embed_recomendacion = discord.Embed(
            title=f"{reaction.emoji} Juegos de {seleccion['genero']}",
            description="Aquí están nuestras recomendaciones:",
            color=discord.Color.green()
        )
        
        for juego in seleccion['juegos']:
            embed_recomendacion.add_field(
                name=f"\u2022 {juego['nombre']}", 
                value=f"{juego['desc']}\n\U0001f517 [Descargar aquí]({juego['link']})", 
                inline=False
            )
        
        await ctx.send(embed=embed_recomendacion)
        
    except:
        await ctx.send("\u23f1\ufe0f Se acabó el tiempo. Usa el comando de nuevo si quieres una recomendación.")

bot.run("MTQ2NjU5NjUzNDkwNzk2MTQ0Nw.GrxtEw.84iZ0kM9SDpuwsD2bSXI3_26Sfixy5rL8DrxW8")
