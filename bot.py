import discord
from discord.ext import commands
from bot_logic import gen_pass
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='$', intents=intents)

def cargar_puntos():
    if os.path.exists('puntos.json'):
        with open('puntos.json', 'r') as f:
            return json.load(f)
    return {}

def guardar_puntos(puntos):
    with open('puntos.json', 'w') as f:
        json.dump(puntos, f, indent=4)

puntos_usuarios = cargar_puntos()

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
async def puntos(ctx):
    user_id = str(ctx.author.id)
    puntos_usuario = puntos_usuarios.get(user_id, 0)
    
    embed = discord.Embed(
        title="\U0001f4b0 Banco de Puntos",
        description=f"{ctx.author.mention}, aquí están tus puntos:",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="\u2b50 Puntos Totales",
        value=f"**{puntos_usuario}** puntos",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f4a1 ¿Cómo ganar puntos?",
        value="Juega $reciclaje y acierta para ganar 5 puntos por respuesta correcta",
        inline=False
    )
    
    embed.set_footer(text="¡Sigue reciclando para ganar más puntos!")
    
    await ctx.send(embed=embed)

@bot.command()
async def ranking(ctx):
    if not puntos_usuarios:
        await ctx.send("¡Aún no hay jugadores en el ranking! Usa $reciclaje para empezar a ganar puntos.")
        return
    
    ranking_ordenado = sorted(puntos_usuarios.items(), key=lambda x: x[1], reverse=True)[:10]
    
    embed = discord.Embed(
        title="\U0001f3c6 Ranking de Recicladores",
        description="¡Los mejores recicladores del servidor!",
        color=discord.Color.gold()
    )
    
    medallas = ["\U0001f947", "\U0001f948", "\U0001f949"]
    
    for i, (user_id, puntos) in enumerate(ranking_ordenado):
        try:
            user = await bot.fetch_user(int(user_id))
            medalla = medallas[i] if i < 3 else f"{i+1}."
            embed.add_field(
                name=f"{medalla} {user.name}",
                value=f"{puntos} puntos",
                inline=False
            )
        except:
            continue
    
    await ctx.send(embed=embed)

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
        name="\U0001f602 $meme",
        value="El bot envía 3 memes divertidos",
        inline=False
    )
    
    embed.add_field(
        name="\u267b\ufe0f $reciclaje",
        value="Mini juego interactivo: ¡Aprende a reciclar y gana 5 puntos por respuesta correcta!",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f4b0 $puntos",
        value="Consulta tus puntos acumulados",
        inline=False
    )
    
    embed.add_field(
        name="\U0001f3c6 $ranking",
        value="Mira el ranking de los mejores recicladores",
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

@bot.command()
async def meme(ctx):
    with open('images/meme1.jpg', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)
    
    with open('images/meme2.jpg', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)
    
    with open('images/meme3.jpg', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def reciclaje(ctx):
    datos_reciclaje = {
        'imag1.jpg': {
            'tipo': 'Botella de Plástico',
            'contenedor_correcto': '\U0001f7e1',
            'nombre_contenedor': 'Amarillo',
            'dato': 'El plástico puede tardar hasta 1000 años en descomponerse. ¡Reciclar una botella ahorra energía para una bombilla durante 3 horas!'
        },
        'imag2.jpg': {
            'tipo': 'Periódico y Papel',
            'contenedor_correcto': '\U0001f535',
            'nombre_contenedor': 'Azul',
            'dato': 'Reciclar una tonelada de papel salva 17 árboles y ahorra 26,000 litros de agua.'
        },
        'imag3.jpg': {
            'tipo': 'Botella de Vidrio',
            'contenedor_correcto': '\U0001f7e2',
            'nombre_contenedor': 'Verde',
            'dato': 'El vidrio es 100% reciclable y puede reciclarse infinitas veces sin perder calidad.'
        },
        'imag4.jpg': {
            'tipo': 'Restos de Comida',
            'contenedor_correcto': '\U0001f7e4',
            'nombre_contenedor': 'Marrón',
            'dato': 'Los residuos orgánicos se convierten en compost, un fertilizante natural que enriquece la tierra.'
        },
        'imag5.jpg': {
            'tipo': 'Lata de Aluminio',
            'contenedor_correcto': '\U0001f7e1',
            'nombre_contenedor': 'Amarillo',
            'dato': 'Reciclar aluminio ahorra un 95% de energía. ¡Una lata reciclada ahorra energía para ver TV durante 3 horas!'
        },
        'imag6.jpg': {
            'tipo': 'Teléfono Móvil Viejo',
            'contenedor_correcto': '\u26a1',
            'nombre_contenedor': 'Punto Limpio',
            'dato': 'Los electrónicos contienen oro, plata y cobre. ¡Reciclarlos evita contaminar el suelo y el agua!'
        }
    }
    
    imagen_random = random.choice(list(datos_reciclaje.keys()))
    info = datos_reciclaje[imagen_random]
    
    contenedores = {
        '\U0001f7e1': 'Amarillo (Plástico y Metal)',
        '\U0001f535': 'Azul (Papel y Cartón)',
        '\U0001f7e2': 'Verde (Vidrio)',
        '\U0001f7e4': 'Marrón (Orgánico)',
        '\u26a1': 'Punto Limpio (Electrónicos)'
    }
    
    embed = discord.Embed(
        title="\u267b\ufe0f \U0001f30d ¡Juego de Reciclaje!",
        description=f"**¿En qué contenedor va este material?**\n\n\U0001f5d1\ufe0f **{info['tipo']}**",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="\U0001f447 Selecciona el contenedor correcto:",
        value="\U0001f7e1 Amarillo\n\U0001f535 Azul\n\U0001f7e2 Verde\n\U0001f7e4 Marrón\n\u26a1 Punto Limpio",
        inline=False
    )
    
    embed.add_field(
        name="\u2b50 Recompensa",
        value="¡Gana 5 puntos si aciertas!",
        inline=False
    )
    
    try:
        with open(f'images/reciclaje/{imagen_random}', 'rb') as f:
            picture = discord.File(f)
        mensaje = await ctx.send(embed=embed, file=picture)
    except FileNotFoundError:
        mensaje = await ctx.send(embed=embed)
    
    for emoji in contenedores.keys():
        await mensaje.add_reaction(emoji)
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in contenedores.keys() and reaction.message.id == mensaje.id
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        
        user_id = str(ctx.author.id)
        
        if str(reaction.emoji) == info['contenedor_correcto']:
            if user_id not in puntos_usuarios:
                puntos_usuarios[user_id] = 0
            
            puntos_usuarios[user_id] += 5
            guardar_puntos(puntos_usuarios)
            
            embed_resultado = discord.Embed(
                title="\u2705 ¡Correcto! ¡Bien hecho!",
                description=f"**{info['tipo']}** va en el contenedor **{info['nombre_contenedor']}** {info['contenedor_correcto']}",
                color=discord.Color.green()
            )
            embed_resultado.add_field(
                name="\U0001f4a1 ¿Sabías que...?",
                value=info['dato'],
                inline=False
            )
            embed_resultado.add_field(
                name="\u2b50 ¡+5 puntos!",
                value=f"Ahora tienes **{puntos_usuarios[user_id]}** puntos totales",
                inline=False
            )
        else:
            embed_resultado = discord.Embed(
                title="\u274c ¡Incorrecto!",
                description=f"**{info['tipo']}** va en el contenedor **{info['nombre_contenedor']}** {info['contenedor_correcto']}, no en {contenedores[str(reaction.emoji)]}",
                color=discord.Color.red()
            )
            embed_resultado.add_field(
                name="\U0001f4a1 Dato importante:",
                value=info['dato'],
                inline=False
            )
            embed_resultado.add_field(
                name="\U0001f4ad No te preocupes",
                value="¡Inténtalo de nuevo para ganar puntos!",
                inline=False
            )
        
        embed_resultado.set_footer(text="Usa $reciclaje para jugar de nuevo | Usa $puntos para ver tu saldo")
        await ctx.send(embed=embed_resultado)
        
    except:
        await ctx.send("\u23f1\ufe0f Se acabó el tiempo. ¡Usa $reciclaje para intentarlo de nuevo!")

bot.run("MTQ2NjU5NjUzNDkwNzk2MTQ0Nw.GrxtEw.84iZ0kM9SDpuwsD2bSXI3_26Sfixy5rL8DrxW8")
