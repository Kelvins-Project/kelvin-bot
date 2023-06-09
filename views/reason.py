import discord
import chat_exporter
import io
from views.dm_close import DMCloseView
class Reason(discord.ui.Modal, title='reason'):

    reason = discord.ui.TextInput(
        label='reason',
        placeholder='your reason here...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        id = interaction.channel.topic
        user = interaction.guild.get_member(int(id))
        logs = interaction.guild.get_channel(1101188264557297814)
        await interaction.response.defer()
        transcript = await chat_exporter.export(interaction.channel)
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript.html",
        )
        await interaction.followup.send('closing ticket...')
        try:
            await user.send(f'your ticket has been closed for the following reason: {self.reason.value}')
            message = await logs.send(file=transcript_file)
            embed = discord.Embed(description=f'{interaction.user.mention} has closed the [ticket](https://mahto.id/chat-exporter?url={message.attachments[0].url})', color=0x2F3136)
            embed.add_field(name='by', value=f'<@{id}>')
            embed.add_field(name='channel name', value=interaction.channel.name)
            embed.add_field(name='reason', value=self.reason.value)

            if transcript is None:
                return
            
            await logs.send(embed=embed)
            await interaction.channel.delete()
        except discord.Forbidden:
            return await interaction.channel.send(f'{user.mention} your mass is done but we couldnt dm u! feel free to leave a rev at https://discord.com/channels/1098191144686473216/1098288401263886417', view=DMCloseView())
    