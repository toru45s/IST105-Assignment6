from django.shortcuts import render
from .forms import NumberForm
from pymongo import MongoClient
import os
from django.http import HttpResponse


client = MongoClient("mongodb://cctb1:cctb2025@54.164.201.206:27017/cctbdb?authSource=cctbdb")
db = client["cctbdb"]
collection = db["inputs"]

def input_view(request):
    result = None
    warning = None

    if request.method == "POST":
        form = NumberForm(request.POST)
        if form.is_valid():
            nums = [form.cleaned_data[key] for key in ['a', 'b', 'c', 'd', 'e']]
            warning = "Warning: Negative values detected!" if any(x < 0 for x in nums) else None

            avg = sum(nums) / len(nums)
            avg_gt_50 = avg > 50
            pos_count = sum(1 for x in nums if x > 0)
            parity = "Even" if (pos_count & 1) == 0 else "Odd"
            sorted_gt_10 = sorted([x for x in nums if x > 10])

            result = {
                "original": nums,
                "sorted": sorted_gt_10,
                "average": avg,
                "average_gt_50": avg_gt_50,
                "positive_count": pos_count,
                "even_or_odd": parity,
            }

            collection.insert_one({"inputs": nums, "results": result})

    else:
        form = NumberForm()

    return render(request, "input_form.html", {"form": form, "result": result, "warning": warning})