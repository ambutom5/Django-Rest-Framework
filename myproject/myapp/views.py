from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class MyClass(APIView):
    def get(self,request):
        return Response(
            {
                "Message" : "Good Morning"
            }
        )

class AdditionView(APIView):
    def post(self,request):
        x = request.data.get("num1")
        y = request.data.get("num2")
        result = x + y
        return Response({
            "Sum" : result
        })

class SubstractionView(APIView):
    def post(self,request):
        x = request.data.get("num1")
        y = request.data.get("num2")
        result = x - y
        return Response({
            "Difference" : result
        })

class MultiplicationView(APIView):
    def post(self,request):
        x = request.data.get("num1")
        y = request.data.get("num2")
        result = x * y
        return Response({
            "Product" : result
        })

class LargestView(APIView):
    def post(self,request):
        x = request.data.get("num1")
        y = request.data.get("num2")
        if x > y:
            return Response({
                "Largest" : x
            })
        else:
            return Response({
                "Largest" : y
            })

class FarenheitView(APIView):
    def post(self,request):
        c = request.data.get("celcius")
        f = (c * 9/5) + 32
        return Response({
            "Farenheit" : f
        })
