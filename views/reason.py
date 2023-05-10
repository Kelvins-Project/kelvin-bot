import discord

class Reason(discord.ui.Modal, title='reason'):

    reason = discord.ui.TextInput(
        label='reason',
        placeholder='your reason here...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        id = interaction.channel.topic
        user = interaction.guild.get_member(int(id))
        await interaction.response.send_message('closing ticket...', ephemeral=True)
        await interaction.channel.delete()
        await user.send(f'your ticket has been closed for the following reason: {self.reason.value}')
        