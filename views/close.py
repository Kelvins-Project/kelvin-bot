import discord
from views.reason import Reason

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='close', style=discord.ButtonStyle.danger, custom_id='persistent_view:close')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

    @discord.ui.button(label='close with reason', style=discord.ButtonStyle.danger, custom_id='persistent_view:close_with_reason')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Reason())
