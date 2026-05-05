from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dataDB import books_col
from .serializers import BookSerializer
from bson import ObjectId 
from django.shortcuts import render

def home(request):
    return render(request, 'inventory/inv.html')

@api_view(['GET', 'POST'])
def book_manager(request):
    """
    Handles Listing all books (with search) and Adding new books.
    """
    if request.method == 'GET':
        query = request.query_params.get('search', '')
        if query:
            # Simple regex search for title or author
            books = list(books_col.find({"$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}}
            ]}))
        else:
            books = list(books_col.find())
        
        # Convert ObjectId to string for JSON serialization
        for b in books: 
            b['_id'] = str(b['_id'])
        return Response(books)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            books_col.insert_one(serializer.validated_data)
            return Response({"msg": "Book Added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def book_detail(request, id):
    """
    Handles Updating and Deleting a specific book by ID.
    """
    try:
        mongo_id = ObjectId(id)
    except:
        return Response({"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        # Use $set to update only the fields provided in request.data
        result = books_col.update_one({"_id": mongo_id}, {"$set": request.data})
        if result.matched_count == 0:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"msg": "Updated successfully"})

    elif request.method == 'DELETE':
        result = books_col.delete_one({"_id": mongo_id})
        if result.deleted_count == 0:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"msg": "Deleted successfully"})
