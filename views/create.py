import discord
from views.close import CloseView

class CreateView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='open', style=discord.ButtonStyle.green, custom_id='persistent_view:confirm')
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description='ticket panel', color=0x2F3136)
        ticket_category = interaction.guild.get_channel(1105961168339738624)
        ticket = await ticket_category.create_text_channel(name=f'{interaction.user.name}-{interaction.user.discriminator}')
        await ticket.edit(topic=interaction.user.id)

        await ticket.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ticket.send(interaction.user.mention, embed=embed, view=CloseView())
        await interaction.response.send_message(ticket.mention, ephemeral=True)
