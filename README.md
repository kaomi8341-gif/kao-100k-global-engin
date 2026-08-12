# K-A-O 100K GLOBAL ENGINE v5
対象アカウント: @kaomi4239
作品: NOAの箱舟

## 目的
NOAの箱舟を海外へ出す際、TikTok Studioの国別実績を使って、
主力国 / 第2候補 / テスト国を自動判定し、字幕・言語・投稿テスト方針を一括生成します。

## 主な機能
- 国別TikTok Studio実績入力
- 12市場の比較
- GLOBAL SCORE
- 主力国 / 第2候補 / テスト国
- NOAの箱舟向け海外投稿パッケージ
- 冒頭0〜3秒、構成、言語、字幕、タイトル、説明文
- 昼枠 / 夜枠のA/Bテスト設計
- TikTok APIで公開済み動画の再生・いいね・コメント・シェア取得
- 100K達成率

## 重要
TikTokの有機For You配信先の国を外部APIで強制指定するツールではありません。
TikTokのレコメンドはTikTok側が決定します。
このアプリは自分の実績を学習し、どの市場向けにローカライズしてテストするかを決める制作支援エンジンです。
GLOBAL SCOREはK-A-Oツール独自指標で、TikTok公式スコアではありません。

## Replit Secrets
TIKTOK_CLIENT_KEY
TIKTOK_CLIENT_SECRET
TIKTOK_REDIRECT_URI=https://YOUR-APP.replit.app/auth/callback/
FLASK_SECRET_KEY=長いランダム文字列
