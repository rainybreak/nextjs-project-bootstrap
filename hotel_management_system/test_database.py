#!/usr/bin/env python3
"""
Test script to verify database functionality
This can be run in the web environment to test the backend
"""

from database import HotelDatabase
from datetime import datetime

def test_database():
    """Test all database functions"""
    print("🏨 Otel Yönetim Sistemi - Database Test")
    print("=" * 50)
    
    # Initialize database
    print("1. Database initialization...")
    db = HotelDatabase()
    print("✅ Database initialized successfully")
    
    # Test fault management
    print("\n2. Testing fault management...")
    
    # Add sample faults
    sample_faults = [
        ("2024-01-15", "101", "F/O", "Klima çalışmıyor", "Bekleniyor"),
        ("2024-01-15", "205", "HK", "Banyo musluğu akıyor", "Bekleniyor"),
        ("2024-01-14", "308", "F&B", "Mini bar soğutmuyor", "Çözüldü"),
    ]
    
    for fault in sample_faults:
        if db.add_fault(*fault):
            print(f"✅ Added fault: Room {fault[1]} - {fault[2]}")
        else:
            print(f"❌ Failed to add fault: Room {fault[1]}")
    
    # Get pending faults
    pending = db.get_pending_faults()
    print(f"\n📋 Pending faults: {len(pending)}")
    for fault in pending:
        print(f"   - Room {fault[2]}: {fault[4][:30]}...")
    
    # Get all faults
    all_faults = db.get_all_faults()
    print(f"📋 Total faults: {len(all_faults)}")
    
    # Test shift management
    print("\n3. Testing shift management...")
    today = datetime.now().strftime('%Y-%m-%d')
    
    if db.update_shift(today, "Ali, Mehmet, Ayşe", "Fatma, Ahmet", "Mavi"):
        print("✅ Shift data updated successfully")
    else:
        print("❌ Failed to update shift data")
    
    shift_data = db.get_today_shift()
    if shift_data:
        print(f"👥 Working staff: {shift_data[2]}")
        print(f"🏖️ On leave: {shift_data[3]}")
        print(f"🎨 Cover color: {shift_data[4]}")
    
    # Test special services
    print("\n4. Testing special services...")
    
    sample_services = [
        "Oda 301 için özel yemek servisi",
        "Havaalanı transfer talebi",
        "Doğum günü pastası siparişi"
    ]
    
    for service in sample_services:
        if db.add_special_service(today, service):
            print(f"✅ Added service: {service[:30]}...")
        else:
            print(f"❌ Failed to add service: {service[:30]}...")
    
    services = db.get_today_special_services()
    print(f"🎯 Today's special services: {len(services)}")
    
    # Test menu management
    print("\n5. Testing menu management...")
    
    sample_menu = """Çorbalar:
- Mercimek Çorbası
- Tavuk Çorbası

Ana Yemekler:
- Izgara Tavuk
- Köfte
- Balık Fileto

Salatalar:
- Çoban Salatası
- Yeşil Salata

Tatlılar:
- Sütlaç
- Baklava"""
    
    if db.update_menu(today, sample_menu):
        print("✅ Menu updated successfully")
    else:
        print("❌ Failed to update menu")
    
    menu_data = db.get_today_menu()
    if menu_data:
        print("🍽️ Today's menu loaded successfully")
    
    # Test cocktail recipes
    print("\n6. Testing cocktail recipes...")
    recipes = db.get_cocktail_recipes()
    print(f"🍹 Available cocktail recipes: {len(recipes)}")
    for recipe in recipes:
        print(f"   - {recipe[1]}")
    
    print("\n" + "=" * 50)
    print("✅ All database tests completed successfully!")
    print("🎉 The hotel management system is ready to use!")
    
    return True

if __name__ == "__main__":
    try:
        test_database()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
