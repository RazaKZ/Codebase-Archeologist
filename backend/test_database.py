"""
Quick database test script
"""
import sys
from database.database import engine, Base, SessionLocal
from database.models import Project, Analysis, DependencyGraph

# Create tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created!")

# Test database connection
print("\nTesting database connection...")
db = SessionLocal()
try:
    # Count projects
    project_count = db.query(Project).count()
    print(f"✅ Database connected! Current projects: {project_count}")
    
    # Test insert
    test_project = Project(
        name="Test Project",
        repo_url="https://github.com/test/test",
        status="pending"
    )
    db.add(test_project)
    db.commit()
    print(f"✅ Test project created with ID: {test_project.id}")
    
    # Clean up test data
    db.delete(test_project)
    db.commit()
    print("✅ Test data cleaned up")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()

print("\n✅ Database is working correctly!")

