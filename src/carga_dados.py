import os
import oracledb
import pandas as pd

# =====================================================================
# 1. CONFIGURAÇÕES DE CONEXÃO COM WALLET
# =====================================================================
DB_USER = "ADMIN"
DB_PASSWORD = "Databytes@123"
DB_DSN = "DATABYTES_HIGH"

WALLET_DIR = r"C:\Users\Jhona\Downloads\VittaVision\VittaVision\data\Wallet"
BASE_DIR = r"C:\Users\Jhona\Downloads\VittaVision\VittaVision"

print("🔄 Lendo os arquivos CSV locais...")
df_pop = pd.read_csv(os.path.join(BASE_DIR, "data", "populacao_2024_sp.csv"), sep=";")
df_int = pd.read_csv(os.path.join(BASE_DIR, "data", "internacoes_2024.csv"), sep=";")
df_leit = pd.read_csv(os.path.join(BASE_DIR, "data", "leitos_2024_por_municipio.csv"), sep=";")

print("🔌 Conectando ao Oracle Autonomous Database com Wallet...")
try:
    connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN,
        config_dir=WALLET_DIR,
        wallet_location=WALLET_DIR,
        wallet_password="Databytes@123"
    )
    cursor = connection.cursor()
    print("✅ Conexão estabelecida com sucesso!\n")

    # -----------------------------------------------------------------
    # 2. CARGA DA TABELA DE POPULAÇÃO
    # -----------------------------------------------------------------
    print("Inserindo dados de População...")
    cursor.execute("DELETE FROM tb_populacao_2024")

    sql_pop = """
        INSERT INTO tb_populacao_2024 (codigo_municipio, codigo_ibge, municipio, populacao)
        VALUES (:1, :2, :3, :4)
    """
    dados_pop = []
    for row in df_pop.itertuples(index=False):
        # Ignora linhas de total ou nulas
        if pd.isna(row[0]) or str(row[0]).strip().lower() in ['total', '']:
            continue
        dados_pop.append((int(row[0]), str(row[1]), str(row[2]), int(row[3])))

    cursor.executemany(sql_pop, dados_pop)
    connection.commit()
    print(f"-> {len(dados_pop)} registros inseridos em tb_populacao_2024.")

    # -----------------------------------------------------------------
    # 3. CARGA DA TABELA DE INTERNAÇÕES
    # -----------------------------------------------------------------
    print("Inserindo dados de Internações...")
    cursor.execute("DELETE FROM tb_internacoes_2024")

    sql_int = """
        INSERT INTO tb_internacoes_2024 (codigo_municipio, municipio, mes, internacoes)
        VALUES (:1, :2, :3, :4)
    """
    dados_int = []
    for row in df_int.itertuples(index=False):
        # Ignora linhas de total, vazias ou onde o código não seja numérico
        val_codigo = str(row[0]).strip()
        if pd.isna(row[0]) or val_codigo.lower() in ['total', ''] or not val_codigo.isdigit():
            continue
            
        cod_mun = int(row[0])
        mun = str(row[1])
        mes = str(row[2])
        inter = int(row[3]) if pd.notnull(row[3]) and str(row[3]).strip().isdigit() else 0
        dados_int.append((cod_mun, mun, mes, inter))

    cursor.executemany(sql_int, dados_int)
    connection.commit()
    print(f"-> {len(dados_int)} registros inseridos em tb_internacoes_2024.")

    # -----------------------------------------------------------------
    # 4. CARGA DA TABELA DE LEITOS
    # -----------------------------------------------------------------
    print("Inserindo dados de Leitos...")
    cursor.execute("DELETE FROM tb_leitos_2024")

    sql_leit = """
        INSERT INTO tb_leitos_2024 (municipio, mes, leitos_existentes, leitos_sus, uti_existente, uti_sus)
        VALUES (:1, :2, :3, :4, :5, :6)
    """
    dados_leit = []
    for row in df_leit.itertuples(index=False):
        # Ignora linhas de total se houver na coluna de município
        val_mun = str(row[0]).strip()
        if pd.isna(row[0]) or val_mun.lower() in ['total', '']:
            continue
            
        mun = val_mun
        mes = str(row[1])
        
        # Função auxiliar segura para converter números lidando com possíveis pontos ou vazios
        def safe_int(val):
            if pd.isna(val) or str(val).strip() == '':
                return 0
            try:
                return int(float(str(val).replace(',', '.')))
            except ValueError:
                return 0

        l_exist = safe_int(row[2])
        l_sus = safe_int(row[3])
        uti_ex = safe_int(row[4])
        uti_s = safe_int(row[5])
        
        dados_leit.append((mun, mes, l_exist, l_sus, uti_ex, uti_s))

    cursor.executemany(sql_leit, dados_leit)
    connection.commit()
    print(f"-> {len(dados_leit)} registros inseridos em tb_leitos_2024.")

    print("\n🎉 Carga de todos os dados realizada com sucesso!")

except Exception as e:
    print(f"⚠️ Erro durante o processo: {e}")

finally:
    if "cursor" in locals():
        cursor.close()
    if "connection" in locals():
        connection.close()
    print("Conexão fechada.")