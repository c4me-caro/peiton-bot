from discord import Embed
from config import config


async def out_permission_embed(ctx):
    await ctx.reply(embed=Embed(
        title="❌ Permisos insuficientes.",
        description="No tienes permisos suficientes para el recurso que has intentado buscar o acceder.",
        color=config.ATTENTION_EMBED_COLOR
    ), ephemeral=True)


async def not_found_embed(ctx):
    await ctx.reply(embed=Embed(
        title="❓ Recurso no encontrado.",
        description="El recurso que has intentado buscar o acceder no se encuentra dentro de los sistemas del bot.",
        color=config.ATTENTION_EMBED_COLOR
    ), ephemeral=True)


async def not_suported_embed(ctx):
    await ctx.reply(embed=Embed(
        title="⛔ Contenido no soportado.",
        description="Parece que has introducido un contenido en un formato que el bot no puede procesar.",
        color=config.ATTENTION_EMBED_COLOR
    ), ephemeral=True)


async def unavalible_embed(ctx):
    await ctx.reply(embed=Embed(
        title="⛔ Contenido no disponible.",
        description="Parece que has pedido al bot una accion que no puede realizar.",
        color=config.ATTENTION_EMBED_COLOR
    ), ephemeral=True)


async def message_embed(ctx, msg):
    reference = ctx.message or ctx
    await ctx.send(embed=Embed(
        title="❕ INFO:",
        description=msg,
        color=config.INFO_EMBED_COLOR
    ))


async def alert_embed(ctx, msg):
    await ctx.send(embed=Embed(
        title="❗ ALERTA:",
        description=msg,
        color=config.ALERT_EMBED_COLOR
    ))
