# import standard modules
from github import Github

# import discord modules
from discord.ext import commands
from discord import Embed


class RepoConnection():
    """ helper class that connects to repo
    """
    def __init__(self, token=None, name=None, **args):
        self.repo = Github(token).get_repo(name)

    def get_issues(self):
        issues = self.repo.get_issues()
        return issues

    def create_issue(self, title, body, label_name=None):
        if label_name is None:
            return self.repo.create_issue(title=title, body=body)
        else:
            try:
                label = self.repo.get_label(label_name)
                return self.repo.create_issue(title=title, body=body, labels=[label])
            except BaseException:
                return self.repo.create_issue(title=title, body=body)


class Repository(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_issue(self, ctx, type, args):
        try:

            if len(args) < 3:
                await ctx.send(f':x: You need to give a repo name, a title and a discord message id to your bug: `!bug <yata|yata-bot> <title> <message id>`')
                return
            elif not (args[0] in ["yata", "yata-bot"] or args[-1].isdigit()):
                await ctx.send(f':x: You need to give a repo name, a title and a discord message id to your bug: `!bug <yata|yata-bot> <title> <message id>`')
                return
            else:
                connection = RepoConnection(token=self.bot.github_token, name=f"kivou-2000607/{args[0]}")
                msg = [_ for _ in await ctx.channel.history().flatten() if _.id == int(args[-1])]
                if len(msg) < 1:
                    await ctx.send(f':x: Message id `{args[-1]}` not found in the channel recent history`')
                    return

                lst = [msg[0].content, "", msg[0].author.display_name, msg[0].jump_url]
                emoji = self.bot.get_emoji(655750002630590464)
                connection.create_issue(" ".join(args[1:-1]), "\n".join(lst), label_name=type)
                await msg[0].add_reaction(emoji)

                await ctx.send(f':white_check_mark: Your {type} has been reported.')

        except BaseException as e:
            await ctx.send(f'Failed to create the issue: {e}')

    @commands.command()
    @commands.has_any_role(679669933680230430, 669682126203125760)
    async def bug(self, ctx, *args):
        await self.create_issue(ctx, "bug", args)

    @commands.command()
    @commands.has_any_role(679669933680230430, 669682126203125760)
    async def suggestion(self, ctx, *args):
        await self.create_issue(ctx, "suggestion", args)
