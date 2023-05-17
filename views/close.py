import discord
from views.reason import Reason
import chat_exporter
import io

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='close', style=discord.ButtonStyle.danger, custom_id='persistent_view:close')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        id = interaction.channel.topic
        user = interaction.guild.get_member(int(id))
        logs = interaction.guild.get_channel(1101188264557297814)
        transcript = await chat_exporter.export(interaction.channel)
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript.html",
        )

        message = await logs.send(file=transcript_file)
        embed = discord.Embed(description=f'{interaction.user.mention} has closed the [ticket](https://mahto.id/chat-exporter?url={message.attachments[0].url})', color=0x2F3136)
        embed.add_field(name='by', value=user.mention)
        embed.add_field(name='channel name', value=interaction.channel.name)
        embed.add_field(name='reason', value='none')

        if transcript is None:
            return
        
        await logs.send(embed=embed)
        await interaction.channel.delete()
        

    @discord.ui.button(label='close with reason', style=discord.ButtonStyle.danger, custom_id='persistent_view:close_with_reason')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Reason())
