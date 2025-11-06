# claude-agent-sample

## 初回セットアップ

### Claude Code インストール

> [!TIP]
> Claude Code をすでにインストールしていてログインしている場合はこの手順をスキップできます。

Claude Code のインストールが必要です。以下を実行してインストールしてください。

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

ref: https://code.claude.com/docs/ja/overview

インストールしたあとは、ログインする必要があります。以下のガイドに従ってログインしてください。

https://code.claude.com/docs/ja/quickstart#%E3%82%B9%E3%83%86%E3%83%83%E3%83%972%EF%BC%9A%E3%82%A2%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%E3%81%AB%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3

### リポジトリセットアップ


リポジトリをクローンした後、以下を実行

```bash
./bin/mise trust && ./bin/mise install
```

## 初回以降のエージェント実行

```bash
./bin/mise run agent
```

