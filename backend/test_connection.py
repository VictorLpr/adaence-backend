#!/usr/bin/env python
"""
Script pour tester la connexion à la base de données Neon
"""
import os
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

def test_database_connection():
    """Test de connexion à la base de données"""
    try:
        with connection.cursor() as cursor:
            # Test basique
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Connexion basique réussie")
            
            # Version PostgreSQL
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Version PostgreSQL: {version}")
            
            # Liste des tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            print(f"✅ Nombre de tables: {len(tables)}")
            
            if tables:
                print("📋 Tables disponibles:")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("⚠️  Aucune table trouvée")
                
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 Test de connexion à la base de données Neon...")
    success = test_database_connection()
    
    if success:
        print("\n🎉 Connexion réussie ! Vous pouvez continuer avec les étapes suivantes.")
    else:
        print("\n💥 Problème de connexion. Vérifiez votre configuration.")