import sys

sys.stdout.reconfigure(encoding='utf-8')
import ccxt
import time
import schedule
import requests
from datetime import datetime


# Function to send messages to Telegram
def send_telegram_message(api_token, chat_id, text):
    api_url = f"https://api.telegram.org/bot{api_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text,
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")


# Replace 'YOUR_API_TOKEN' and 'YOUR_CHAT_ID' with your actual API token and chat ID
api_token = '6092684310:AAFOUOWX74icIr_VcJdkKH6skhVvTdAZKrA'
chat_id = '-1002053630518'

# Initialize MXC exchange
exchange = ccxt.mexc()

# List of 30 most famous coins
symbols = [
    'AAVE_USDT', 'ACE_USDT', 'ACH_USDT', 'ADA_USDT', 'AERGO_USDT',
    'AGIX_USDT', 'AGI_USDT', 'AGLD_USDT','AI_USDT', 'AKRO_USDT', 'ALGO_USDT',
    'ALICE_USDT', 'ALPACA_USDT', 'ALPHA_USDT','ALT_USDT', 'AMB_USDT', 'ANKR_USDT',
    'ANT_USDT', 'APE_USDT', 'API3_USDT', 'APT_USDT', 'ARB_USDT',
    'ARKM_USDT', 'ARK_USDT', 'ARPA_USDT', 'AR_USDT',
    'ASTR_USDT','ATA_USDT',  'ATOM_USDT', 'AUCTION_USDT','AUDIO_USDT',
    'AVAX_USDT', 'AXS_USDT', 'BADGER_USDT', 'BAKE_USDT',
    'BAL_USDT', 'BAND_USDT', 'BAT_USDT', 'BCH_USDT', 'BEAMX_USDT',
    'BEL_USDT', 'BICO_USDT', 'BIGTIME_USDT', 'BLUR_USDT', 'BLZ_USDT',
    'BNB_USDT', 'BNT_USDT',  'BNX/USDT','BOBA_USDT', 'BOND_USDT',
    'BONE_USDT', 'BSV_USDT', 'BSW_USDT',  'BTC_USDT',
    'C98_USDT', 'CAKE_USDT', 'CEEK_USDT', 'CELO_USDT', 'CELR_USDT',
    'CEL_USDT', 'CETUS_USDT', 'CFX_USDT',  'CHR_USDT','CHZ_USDT',
    'CKB_USDT',  'COMBO_USDT', 'COMP_USDT', 'CORE_USDT',
    'COTI_USDT', 'CRO_USDT', 'CRV_USDT', 'CSPR_USDT', 'CTC_USDT',
    'CTK_USDT', 'CTSI_USDT',  'CVC_USDT','CVX_USDT', 'CYBER_USDT',
    'DAR_USDT', 'DASH_USDT',  'DATA_USDT', 'DENT_USDT','DMAIL_USDT','DODO_USDT',
    'DOGE_USDT', 'DOT_USDT', 'DUSK_USDT', 'DYDX_USDT','DYM_USDT', 'EDU_USDT',
    'EGLD_USDT', 'ENJ_USDT', 'ENS_USDT', 'EOS_USDT', 'ETC_USDT',
    'ETHW_USDT', 'ETH_USDT', 'FET_USDT',  'FIL/USDT',
    'FITFI_USDT', 'FLM_USDT', 'FLOKI_USDT', 'FLOW_USDT', 'FLR_USDT',
    'FORTH_USDT', 'FRONT_USDT', 'FTM_USDT', 'FTT_USDT', 'FUN_USDT',
    'FXS_USDT', 'GALA_USDT', 'GAL_USDT','GAS_USDT',  'GFT_USDT',
    'GLMR_USDT', 'GMT_USDT', 'GMX_USDT', 'GODS_USDT', 'GROK_USDT',
    'GRT_USDT', 'GTC_USDT', 'HBAR_USDT', 'HFT_USDT', 'HIFI_USDT',
    'HIGH_USDT',  'HNT_USDT','HOOK_USDT', 'HOT_USDT',
    'ICP_USDT', 'ICX_USDT', 'IDEX_USDT', 'ID_USDT',
    'ILV_USDT', 'IMX_USDT', 'INJ_USDT', 'IOST_USDT','IOTA_USDT',
    'IOTX_USDT', 'JASMY_USDT', 'JOE_USDT', 'JTO_USDT','JUP_USDT', 'KAS_USDT',
    'KAVA_USDT', 'KDA_USDT','KEY_USDT', 'KLAY_USDT', 'KNC_USDT',
    'KSM_USDT',  'LDO_USDT', 'LEVER_USDT',
    'LINA_USDT', 'LINK_USDT', 'LIT_USDT', 'LOOKS_USDT', 'LOOM_USDT',
    'LPT_USDT', 'LQTY_USDT', 'LRC_USDT', 'LSK_USDT','LTC_USDT', 'LUNA/USDT',
    'LUNC_USDT', 'MAGIC_USDT', 'MANA_USDT', 'MANTA_USDT','MASK_USDT', 'MATIC_USDT','MAVIA_USDT',
    'MAV_USDT', 'MBL_USDT', 'MDT_USDT', 'MEME_USDT','METIS_USDT', 'MINA_USDT',
    'MKR_USDT', 'MNT_USDT','MOVR_USDT', 'MTL_USDT', 'MUBI_USDT',
   'MYRO_USDT', 'NEAR_USDT', 'NEO_USDT', 'NFP_USDT',
    'NKN_USDT', 'NMR_USDT', 'NTRN_USDT', 'OCEAN_USDT', 'OGN_USDT',
    'OMG_USDT', 'OM_USDT','ONDO_USDT','ONE_USDT', 'ONG_USDT', 'ONT_USDT', 'OP_USDT',
    'ORBS_USDT','ORDI_USDT', 'OXT_USDT', 'PAXG_USDT', 'PENDLE_USDT',
    'PEOPLE_USDT', 'PEPE_USDT', 'PERP_USDT', 'PHB_USDT',
    'POLYX_USDT','POWR_USDT','PROM_USDT','PYTH_USDT', 'QI_USDT',
    'QNT_USDT', 'QTUM_USDT', 'RAD_USDT', 'RARE_USDT',
    'RDNT_USDT', 'REEF_USDT', 'REN_USDT','REQ_USDT', 'RIF_USDT',
    'RLC_USDT', 'RNDR_USDT','RON_USDT', 'ROSE_USDT', 'RPL_USDT', 'RSR_USDT',
    'RSS3_USDT','RUNE_USDT', 'RVN_USDT',  'SAND_USDT', 'SATS_USDT',
    'SCRT_USDT', 'SC_USDT', 'SEI_USDT', 'SFP_USDT', 'SHIB_USDT','SILLY_USDT',
    'SKL_USDT', 'SLP_USDT', 'SNT_USDT', 'SNX_USDT',
    'SOL_USDT', 'SPELL_USDT','SSV_USDT',  'STEEM_USDT',
    'STG_USDT','STMX_USDT', 'STORJ_USDT', 'STPT_USDT',
    'STX_USDT', 'SUI_USDT', 'SUN_USDT','SUPER_USDT',  'SUSHI_USDT',
    'SWEAT_USDT','SXP_USDT', 'TAO_USDT', 'THETA_USDT',
    'TIA_USDT',  'TLM_USDT', 'TOKEN_USDT', 'TOMI_USDT',
    'TON/USDT', 'TRB_USDT', 'TRU_USDT', 'TRX_USDT', 'TURBO_USDT',
    'TWT_USDT', 'T_USDT', 'UMA_USDT',
    'UNFI_USDT', 'UNI_USDT', 'VET_USDT',  'VRA_USDT',
    'WAVES_USDT','WAXP_USDT', 'WIF_USDT',
       'WLD_USDT','WOO_USDT',
    'WOO_USDT',  'XCH_USDT', 'XCN_USDT', 'XEC_USDT',
    'XEM_USDT', 'XLM_USDT','XMR_USDT','XNO_USDT',
       'XRP_USDT',
    'XTZ_USDT', 'XVG_USDT', 'YFI_USDT',
    'YGG_USDT', 'ZEC_USDT', 'ZEN_USDT', 'ZETA_USDT', 'ZIL_USDT',
    'ZRX_USDT', 'ZKF_USDT',
]
green_circle_emoji = "\U0001F7E2"
red_circle_emoji = "\U0001F534"
hammer_emoji = "\U0001F528"
interval = '15m'

while True:
    try:

        def job():

            for symbol in symbols:
                # Get candle data
                candles = exchange.fetch_ohlcv(symbol, interval)

                # Check if candles is not None and is an iterable list
                if candles is not None and isinstance(candles, list):
                    # Extract the open, close, high, and low values of the candle
                    opens = [candle[1] for candle in candles]
                    closes = [candle[4] for candle in candles]
                    highs = [candle[2] for candle in candles]
                    lows = [candle[3] for candle in candles]

                    # Check for the "Hammer" candlestick pattern with more specific conditions
                    if (
                            len(closes) >= 15  # Ensure there are at least 4 candles for analysis
                            and lows[-1] < lows[-40]
                            and lows[-1] < lows[-2]  # Ensure the low of the current candle is lower than the previous candle
                            and lows[-1] < lows[-3]  # Ensure the low of the current candle is lower than the third previous candle
                            and lows[-1] < lows[-4]
                            and lows[-1] < lows[-7]  # Ensure the low of the current candle is lower than the fourth previous candle
                            and lows[-1] < lows[-10]
                            and lows[-1] < lows[-15]
                            and lows[-1] < lows[-18]
                            and lows[-1] < lows[-20]
                            and lows[-1] < lows[-25]
                            and closes[-1] < closes[-2]  # Ensure the close is under the third previous close
                            and closes[-1] < closes[-3]  # Ensure the close is under the third previous close
                            and closes[-1] < closes[-4]  # Ensure the close is under the third previous close
                            and closes[-1] < closes[-6]
                            and closes[-1] < closes[-8]
                            and closes[-1] < closes[-10]
                            and closes[-1] < closes[-12]
                            and closes[-1] < closes[-14]
                            and closes[-1] < closes[-16]
                            and highs[-1] == opens[-1]  # Ensure the high is equal to the open, indicating no upper shadow
                            and (closes[-1] - lows[-1]) >= 0.6 * (highs[-1] - lows[-1])
                    # Ensure the lower shadow is at least 60% of the total candle height
                    ):

                        message_text = f"{hammer_emoji} {green_circle_emoji} {symbol}{green_circle_emoji} LONG"
                        send_telegram_message(api_token, chat_id, message_text)
                        print(f"15  Hammer for {symbol}. Analysis complete.")
                        print("___________________________________")
                    if (
                            len(closes) >= 9  # Ensure there are at least 4 candles for analysis
                            and highs[-1] > highs[-40]
                            and highs[-1] > highs[-2]  # Ensure the high of the current candle is higher than the previous candle
                            and highs[-1] > highs[-5]  # Ensure the high of the current candle is higher than the third previous candle
                            and highs[-1] > highs[-8]  # Ensure the high of the current candle is higher than the fourth previous candle
                            and highs[-1] > highs[-11]
                            and highs[-1] > highs[-15]
                            and highs[-1] > highs[-20]
                            and highs[-1] > highs[-25]
                            and highs[-1] > highs[-30]
                            and highs[-1] > highs[-35]
                            and closes[-1] > closes[-2]  # Ensure the close is above the previous close
                            and closes[-1] > closes[-3]  # Ensure the close is above the second previous close
                            and closes[-1] > closes[-4]  # Ensure the close is above the third previous close
                            and closes[-1] > closes[-8]
                            and closes[-1] > closes[-14]
                            and closes[-1] > closes[-20]
                            and closes[-1] > closes[-25]
                            and closes[-1] > closes[-30]
                            and lows[-1] == opens[-1]  # Ensure the low is equal to the open, indicating no lower shadow
                            and (highs[-1] - closes[-1]) >= 0.6 * (highs[-1] - lows[-1])
                    # Ensure the upper shadow is at least 70% of the total candle height

                    ):
                        message_text = f"{hammer_emoji}{red_circle_emoji} {symbol}{red_circle_emoji} SHORT"
                        send_telegram_message(api_token, chat_id, message_text)
                        print(f"15m Inverted Hammer for {symbol}. Analysis complete.")
                        print("___________________________________")

                        # Send a completion message after analyzing all symbols



        current_time = datetime.now().strftime("%M:%S")

        schedule.every().hour.at("12:30").do(job)

        schedule.every().hour.at("28:30").do(job)

        schedule.every().hour.at("42:30").do(job)

        schedule.every().hour.at("57:30").do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        # Optionally, you can log the error to a file or take other actions
        time.sleep(600)