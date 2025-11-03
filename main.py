import asyncio
import sys
from typing import Any, Dict
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    SystemMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

# シンプルな計算エージェントのシステムプロンプト
SYSTEM_PROMPT = """あなたはシンプルな計算エージェントです。足し算と引き算のみを実行できます。

<role>
あなたは教育用の計算アシスタントとして、以下の機能のみを提供します：
- 足し算（add）: 2つの数値を足します
- 引き算（sub）: 2つの数値を引きます
</role>

<core_principles>
1. シンプルさ：計算機能のみに集中
2. 正確性：計算結果は常に正確に
3. 親切さ：わかりやすく結果を説明
</core_principles>

<boundaries>
以下のリクエストは処理できません：
- 掛け算や割り算などの他の演算
- 複雑な数学的計算
- 計算以外のタスク
</boundaries>

<tools_specification>
利用可能なツール：
- add: 2つの数値を足します（a: 数値, b: 数値）
- sub: 2つの数値を引きます（a: 数値, b: 数値）
</tools_specification>

重要：計算機能の範囲内で最高のサービスを提供し、範囲外のリクエストは丁寧に説明してください。"""


@tool(
    "add",
    "2つの数値を足し算します。",
    {
        "a": float,  # 1つ目の数値
        "b": float,  # 2つ目の数値
    },
)
async def add(args: Dict[str, Any]) -> Dict[str, Any]:
    """足し算を実行"""
    a = args.get("a")
    b = args.get("b")

    if a is None or b is None:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "❌ エラー: 2つの数値を指定してください。",
                }
            ]
        }

    result = a + b

    return {
        "content": [
            {
                "type": "text",
                "text": f"✅ 計算結果: {a} + {b} = {result}",
            }
        ]
    }


@tool(
    "sub",
    "2つの数値を引き算します。",
    {
        "a": float,  # 1つ目の数値
        "b": float,  # 2つ目の数値
    },
)
async def sub(args: Dict[str, Any]) -> Dict[str, Any]:
    """引き算を実行"""
    a = args.get("a")
    b = args.get("b")

    if a is None or b is None:
        return {
            "content": [
                {
                    "type": "text",
                    "text": "❌ エラー: 2つの数値を指定してください。",
                }
            ]
        }

    result = a - b

    return {
        "content": [
            {
                "type": "text",
                "text": f"✅ 計算結果: {a} - {b} = {result}",
            }
        ]
    }


def display_message(msg):
    """メッセージをRichで美しく表示"""
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                claude_panel = Panel(
                    Text(block.text, style="white"),
                    title="🤖 計算エージェント",
                    title_align="left",
                    border_style="blue",
                    padding=(0, 1),
                )
                console.print(claude_panel)
            elif isinstance(block, ToolUseBlock):
                tool_info = f"[bold cyan]ツール:[/bold cyan] {block.name}"
                if block.input:
                    input_str = ", ".join([f"{k}={v}" for k, v in block.input.items()])
                    tool_info += f"\n[dim]入力: {input_str}[/dim]"

                tool_panel = Panel(
                    tool_info,
                    title="🔧 ツール実行",
                    title_align="left",
                    border_style="green",
                    padding=(0, 1),
                )
                console.print(tool_panel)
    elif isinstance(msg, SystemMessage):
        pass
    elif isinstance(msg, ResultMessage):
        if msg.total_cost_usd:
            console.print(f"💰 [dim]コスト: ${msg.total_cost_usd:.6f}[/dim]")


async def process_claude_response(client, prompt_text: str):
    """Claudeの応答をSpinnerと共に処理"""
    await client.query(prompt_text)

    with console.status("[bold green]🤖 計算中...", spinner="dots") as status:
        async for message in client.receive_response():
            status.stop()
            display_message(message)
            if isinstance(message, (AssistantMessage, SystemMessage)):
                status.start()


async def interactive_mode():
    """インタラクティブモード"""
    welcome_text = """🔢 シンプル計算エージェントへようこそ！

このエージェントは足し算と引き算ができます。
例: 「5と3を足して」「10から4を引いて」

[dim]終了方法: 'quit', 'exit', 'q'[/dim]"""

    welcome_panel = Panel(
        welcome_text,
        title="🚀 計算エージェント",
        title_align="center",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(welcome_panel)

    # 定義したツールを利用したMCPサーバーを作成
    calc_server = create_sdk_mcp_server(
        name="calculator",
        version="1.0.0",
        tools=[add, sub],  # 定義した関数を指定
    )

    # エージェントオプションの設定
    options = ClaudeAgentOptions(
        mcp_servers={"calculator": calc_server},
        allowed_tools=[
            "mcp__calculator__add",
            "mcp__calculator__sub",
        ],
        system_prompt=SYSTEM_PROMPT,
        permission_mode="default",
        setting_sources=[],
    )

    # クライアントをループの外で作成し、セッション全体で再利用
    async with ClaudeSDKClient(options=options) as client:
        session_id = None

        while True:
            try:
                console.print()
                user_input = Prompt.ask("[bold cyan]💬 あなた[/bold cyan]").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    goodbye_panel = Panel(
                        "👋 ありがとうございました！",
                        title="さようなら",
                        title_align="center",
                        border_style="green",
                        padding=(0, 2),
                    )
                    console.print(goodbye_panel)
                    break

                if not user_input:
                    continue

                # 同じクライアントを使って会話を続ける
                await process_claude_response(client, user_input)

            except KeyboardInterrupt:
                goodbye_panel = Panel(
                    "👋 ありがとうございました！",
                    title="中断されました",
                    title_align="center",
                    border_style="yellow",
                    padding=(0, 2),
                )
                console.print(goodbye_panel)
                break
            except Exception as e:
                error_panel = Panel(
                    f"❌ エラーが発生しました: {e}",
                    title="エラー",
                    title_align="left",
                    border_style="red",
                    padding=(0, 1),
                )
                console.print(error_panel)


async def main():
    try:
        await interactive_mode()
    except Exception as e:
        error_panel = Panel(
            f"❌ 予期しないエラーが発生しました: {e}",
            title="致命的エラー",
            title_align="left",
            border_style="red",
            padding=(0, 1),
        )
        console.print(error_panel, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
