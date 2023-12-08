import asyncio
import random
import os
import sqlite3
import math
import json
from ..utils.resource.RESOURCE_PATH import MAIN_PATH
DB_PATH = os.path.expanduser(MAIN_PATH / 'pokemon.db')

class PokeCounter:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_table()
        self._create_table_map()
        self._create_table_group()
        self._create_table_egg()
        self._create_table_prop()
        self._create_table_star()
        self._create_table_starrush()
    
    def _connect(self):
        return sqlite3.connect(DB_PATH)
    
    def _create_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_TABLE
                          (UID             TEXT   NOT NULL,
                           BIANHAO         INT    NOT NULL,
                           LEVEL           INT    NOT NULL,
                           EXP             INT    NOT NULL,
                           GT_HP           INT    NOT NULL,
                           GT_ATK          INT    NOT NULL,
                           GT_DEF          INT    NOT NULL,
                           GT_STK          INT    NOT NULL,
                           GT_SEF          INT    NOT NULL,
                           GT_SPD          INT    NOT NULL,
                           NL_HP           INT    NOT NULL,
                           NL_ATK          INT    NOT NULL,
                           NL_DEF          INT    NOT NULL,
                           NL_STK          INT    NOT NULL,
                           NL_SEF          INT    NOT NULL,
                           NL_SPD          INT    NOT NULL,
                           XINGGE          TEXT   NOT NULL,
                           JINENG          TEXT   NOT NULL,
                           PRIMARY KEY(UID,BIANHAO));''')
        except:
            raise Exception('创建表发生错误')
    
    def _create_table_map(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_MAP
                          (UID             TEXT   NOT NULL,
                           HUIZHANG        TEXT   NOT NULL,
                           MAP_NAME        TEXT   NOT NULL,
                           NICKNAME        TEXT   NOT NULL,
                           PRIMARY KEY(UID));''')
        except:
            raise Exception('创建表发生错误')
    
    def _create_table_group(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_TEAM
                          (UID             TEXT   NOT NULL,
                           TEAM            TEXT   NOT NULL,
                           PRIMARY KEY(UID));''')
        except:
            raise Exception('创建表发生错误')
    
    def _create_table_egg(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_EGG
                          (UID             TEXT   NOT NULL,
                           BIANHAO         INT    NOT NULL,
                           NUM             INT    NOT NULL,
                           PRIMARY KEY(UID, BIANHAO));''')
        except:
            raise Exception('创建表发生错误')
    
    def _create_table_prop(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_PROP
                          (UID             TEXT   NOT NULL,
                           PROP            TEXT   NOT NULL,
                           NUM             INT    NOT NULL,
                           PRIMARY KEY(UID, PROP));''')
        except:
            raise Exception('创建表发生错误')
    
    def _create_table_star(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_STAR
                          (UID             TEXT   NOT NULL,
                           BIANHAO         INT    NOT NULL,
                           TYPE            INT    NOT NULL,
                           PRIMARY KEY(UID, BIANHAO));''')
        except:
            raise Exception('创建表发生错误')
    
    def _create_table_starrush(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS POKEMON_STARRUSH
                          (UID             TEXT   NOT NULL,
                           NUM             INT    NOT NULL,
                           PRIMARY KEY(UID));''')
        except:
            raise Exception('创建表发生错误')
    
    def update_pokemon_star(self,uid,bianhao,startype=0):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_STAR (UID,BIANHAO,TYPE) VALUES (?,?,?)", (uid, bianhao,startype)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def get_pokemon_star(self,uid,bianhao):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT TYPE FROM POKEMON_STAR WHERE UID='{uid}' AND BIANHAO={bianhao}").fetchall()
                if r:
                    return r[0][0]
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _delete_poke_star(self, uid):
        with self._connect() as conn:
            conn.execute(f"DELETE FROM POKEMON_STAR WHERE UID='{uid}'").fetchall()
    
    def _delete_poke_star_bianhao(self, uid, bianhao):
        with self._connect() as conn:
            conn.execute(f"DELETE FROM POKEMON_STAR WHERE UID='{uid}' AND BIANHAO={bianhao}").fetchall()
    
    def get_pokemon_starrush(self,uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT TYPE FROM POKEMON_PROP WHERE UID='{uid}' AND BIANHAO={bianhao}").fetchall()
                if r:
                    return r[0][0]
                else:
                    self.update_pokemon_starrush(uid,0)
                    return 0
        except:
            raise Exception('查找表发生错误') 
    
    def update_pokemon_starrush(self,uid,num):
        rushnum = self.get_pokemon_starrush(uid) + num
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_STARRUSH (UID,NUM) VALUES (?,?)", (uid, rushnum)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def new_pokemon_starrush(self,uid):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_STARRUSH (UID,NUM) VALUES (?,?)", (uid, 0)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def get_pokemon_prop_list(self, uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT PROP,NUM FROM POKEMON_PROP WHERE UID='{uid}' AND NUM>0 ORDER BY NUM").fetchall()
                if r:
                    return r
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _new_pokemon_prop(self, uid, propname):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_PROP (UID,PROP,NUM) VALUES (?,?,?)", (uid, propname,0)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def _get_pokemon_prop(self, uid, propname):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT NUM FROM POKEMON_PROP WHERE UID='{uid}' AND PROP='{propname}'").fetchall()
                if r:
                    return r[0][0]
                else:
                    self._new_pokemon_prop(uid, propname)
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _add_pokemon_prop(self, uid, propname, num):
        now_num = self._get_pokemon_prop(uid, propname) + num
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_PROP (UID,PROP,NUM) VALUES (?,?,?)", (uid, propname,now_num)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def _add_pokemon_group(self, uid, pokemon_list):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_TEAM (UID,TEAM) VALUES (?,?)", (uid, pokemon_list)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def get_pokemon_group(self, uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT TEAM FROM POKEMON_TEAM WHERE UID='{uid}'").fetchall()
                if r:
                    return r[0][0]
                else:
                    return ''
        except:
            raise Exception('查找表发生错误')
    
    def delete_pokemon_group(self, uid):
        with self._connect() as conn:
            conn.execute(
                f"DELETE FROM POKEMON_TEAM WHERE UID='{uid}'"
            ).fetchall()
    
    def _add_pokemon_egg(self, uid, bianhao, use_num):
        eggnum = int(self.get_pokemon_egg(uid, bianhao)) + int(use_num)
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_EGG (UID,BIANHAO,NUM) VALUES (?,?,?)", (uid, bianhao, eggnum)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def delete_pokemon_egg_bianhao(self, uid, bianhao):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_EGG SET NUM=0 WHERE UID='{uid}' AND BIANHAO={bianhao}"
                )  
        except:
            raise Exception('更新表发生错误')
    
    def get_pokemon_egg(self, uid, bianhao):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT NUM FROM POKEMON_EGG WHERE UID='{uid}' AND BIANHAO={bianhao}").fetchall()
                if r:
                    return r[0][0]
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def get_pokemon_egg_num(self, uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT COUNT(BIANHAO) AS EGGNUM FROM POKEMON_EGG WHERE UID='{uid}' AND NUM>0").fetchall()
                if r:
                    return r[0][0]
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def get_pokemon_egg_list(self, uid, page = 0):
        num = 30
        startnum = num * page
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT BIANHAO,NUM FROM POKEMON_EGG WHERE UID='{uid}' AND NUM>0 ORDER BY NUM desc,BIANHAO ASC LIMIT {startnum},{num}").fetchall()
                if r:
                    return r
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def delete_pokemon_egg(self, uid):
        
        with self._connect() as conn:
            conn.execute(
                f"DELETE FROM POKEMON_EGG WHERE UID='{uid}'"
            ).fetchall()
    
    def _get_map_now(self,uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT HUIZHANG,MAP_NAME,NICKNAME FROM POKEMON_MAP WHERE UID='{uid}'").fetchall()
                if r:
                    return r[0]
                else:
                    return [0,'',0]
        except:
            raise Exception('查找表发生错误')
    
    def _get_map_info_nickname(self,nickname):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT HUIZHANG,MAP_NAME,UID FROM POKEMON_MAP WHERE NICKNAME='{nickname}'").fetchall()
                if r:
                    return r[0]
                else:
                    return [0,'',0]
        except:
            raise Exception('查找表发生错误')
    
    def _add_map_now(self,uid,map_name):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_MAP SET MAP_NAME='{map_name}' WHERE UID='{uid}'"
                )  
        except:
            raise Exception('更新表发生错误')
    
    def _new_map_info(self,uid,map_name,nickname):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_MAP (UID,HUIZHANG,MAP_NAME,NICKNAME) VALUES (?,?,?,?)", (uid, 0, map_name,nickname)
                )  
        except:
            raise Exception('更新表发生错误')
    
    def _update_map_name(self,uid,nickname):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_MAP SET NICKNAME='{nickname}' WHERE UID='{uid}'"
                )  
        except:
            raise Exception('更新表发生错误')
    
    def _update_map_huizhang(self,uid,huizhang):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_MAP SET HUIZHANG={huizhang} WHERE UID='{uid}'"
                )  
        except:
            raise Exception('更新表发生错误')
    
    def delete_pokemon_map(self, uid):
        with self._connect() as conn:
            conn.execute(
                f"DELETE FROM POKEMON_MAP  WHERE UID='{uid}'"
            ).fetchall()
    
    def _add_huizhang_now(self,uid,huizhang):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_MAP SET HUIZHANG='{huizhang}' WHERE UID='{uid}'"
                )  
        except:
            raise Exception('更新表发生错误')
    
    def _add_pokemon_info(self, uid, bianhao, pokemon_info, exp = 0):
        level, gt_hp, gt_atk, gt_def, gt_stk, gt_sdf, gt_spd, nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd, xingge, jineng = pokemon_info
        #print(pokemon_info)
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO POKEMON_TABLE (UID,BIANHAO,LEVEL,EXP,GT_HP,GT_ATK,GT_DEF,GT_STK,GT_SEF,GT_SPD,NL_HP,NL_ATK,NL_DEF,NL_STK,NL_SEF,NL_SPD,XINGGE,JINENG) \
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (uid, bianhao, level, exp, gt_hp, gt_atk, gt_def, gt_stk, gt_sdf, gt_spd, nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd, xingge, jineng)
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _add_pokemon_level(self, uid, bianhao, level, exp):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_TABLE SET LEVEL=?, EXP=? WHERE UID='{uid}' AND BIANHAO=?",(level, exp, bianhao)
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _add_pokemon_nuli(self, uid, bianhao, nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_TABLE SET NL_HP=?,NL_ATK=?,NL_DEF=?,NL_STK=?,NL_SEF=?,NL_SPD=? WHERE UID='{uid}' AND BIANHAO=?",
                    (nl_hp, nl_atk, nl_def, nl_stk,nl_sef, nl_spd, bianhao)
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _add_pokemon_jineng(self, uid, bianhao, jineng):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_TABLE SET JINENG='{jineng}' WHERE UID='{uid}' AND BIANHAO={bianhao}"
                )
                  
        except:
            raise Exception('更新表发生错误')
    
    def _add_pokemon_xingge(self, uid, bianhao, xingge):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_TABLE SET XINGGE='{xingge}' WHERE UID='{uid}' AND BIANHAO={bianhao}"
                )
                  
        except:
            raise Exception('更新表发生错误')
    
    def _add_pokemon_id(self, uid, bianhao, changeid):
        try:
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE POKEMON_TABLE SET BIANHAO='{changeid}' WHERE UID='{uid}' AND BIANHAO={bianhao}"
                )
                  
        except:
            raise Exception('更新表发生错误')
            
    def _get_pokemon_info(self, uid, bianhao):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT LEVEL,GT_HP,GT_ATK,GT_DEF,GT_STK,GT_SEF,GT_SPD,NL_HP,NL_ATK,NL_DEF,NL_STK,NL_SEF,NL_SPD,XINGGE,JINENG,EXP FROM POKEMON_TABLE WHERE UID='{uid}' AND BIANHAO={bianhao}").fetchall()
                if r:
                    return r[0]
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _get_pokemon_level(self, uid, bianhao):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT LEVEL,EXP FROM POKEMON_TABLE WHERE UID='{uid}' AND BIANHAO={bianhao}").fetchall()
                if r:
                    return r[0]
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _get_pokemon_num(self, uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT COUNT(BIANHAO) AS NUM FROM POKEMON_TABLE WHERE UID='{uid}'").fetchall()
                if r:
                    return r[0][0]
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _get_pokemon_list(self, uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT BIANHAO,LEVEL FROM POKEMON_TABLE WHERE UID='{uid}' ORDER BY LEVEL desc LIMIT 20").fetchall()
                if r:
                    return r
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _get_my_pokemon(self, uid):
        try:
            with self._connect() as conn:
                r = conn.execute(
                    f"SELECT BIANHAO FROM POKEMON_TABLE WHERE UID='{uid}' ORDER BY LEVEL desc").fetchall()
                if r:
                    return r
                else:
                    return 0
        except:
            raise Exception('查找表发生错误')
    
    def _delete_poke_info(self, uid):
        with self._connect() as conn:
            conn.execute(f"DELETE FROM POKEMON_TABLE WHERE UID='{uid}'").fetchall()
    
    def _delete_poke_bianhao(self, uid, bianhao):
        with self._connect() as conn:
            conn.execute(
                f"DELETE FROM POKEMON_TABLE WHERE UID='{uid}' AND BIANHAO={bianhao}"
            ).fetchall()