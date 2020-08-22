from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lists.models import Item, List

User = get_user_model()


class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item(list=list_)
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="Duplicate")
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text="Duplicate")
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list_first = List.objects.create()
        list_second = List.objects.create()
        Item.objects.create(list=list_first, text="Duplicate")
        item = Item(list=list_second, text="Duplicate")
        item.full_clean()  # should not throw an exception

    def test_list_ordering(self):
        list_first = List.objects.create()
        item_first = Item.objects.create(list=list_first, text="i1")
        item_second = Item.objects.create(list=list_first, text="item 2")
        item_third = Item.objects.create(list=list_first, text="3")
        self.assertEqual(
            list(Item.objects.all()), [item_first, item_second, item_third]
        )

    def test_string_representation(self):
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text="new item text")
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "new item text")
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text="new item text", owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owners(self):
        List(owner=User())

    def test_list_owner_is_optional(self):
        List().full_clean()

    def test_create_new_returns_list_object(self):
        returned = List.create_new(first_item_text="new item text")
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)
    
    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')
